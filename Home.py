import streamlit as st
from PIL import Image
import cv2
import numpy as np
import io
from fpdf import FPDF
import base64
import os
from datetime import datetime
from inference_sdk import InferenceHTTPClient

# ===============================
# 页面配置
# ===============================
st.set_page_config(
    page_title="管道缺陷智能检测系统",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main { background-color: #f5f7fb; }
    .stApp { background-color: #f5f7fb; }
    h1, h2, h3 { color: #1e3c72; }
    .stButton>button {
        background-color: #1e3c72;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #2a5298;
        transform: scale(1.02);
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ===============================
# 初始化 session_state
# ===============================
if 'detection_done' not in st.session_state:
    st.session_state.detection_done = False
if 'predictions_json' not in st.session_state:
    st.session_state.predictions_json = None
if 'output_image_path' not in st.session_state:
    st.session_state.output_image_path = None
if 'input_image_path' not in st.session_state:
    st.session_state.input_image_path = None
if 'collected_predictions' not in st.session_state:
    st.session_state.collected_predictions = None

# ===============================
# Roboflow Inference 客户端配置
# ===============================
API_KEY = "hyS6omDevAuBj3UN89vP"   
MODEL_ID = "gas-pipelines/2"

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY
)

# ===============================
# 推理函数（将结果存入 session_state）
# ===============================
def run_inference_and_save(uploaded_img_path):
    # 显示模型信息
    with st.expander("📊 Model Information", expanded=False):
        col1, col2 = st.columns(2)
        col1.write(f"**Model**: {MODEL_ID}")
        col1.write(f"**Type**: Instance Segmentation (with bounding boxes)")
        col2.write(f"**Inference API**: Roboflow Serverless")
        col2.write(f"**Framework**: YOLOv11-based")

    st.markdown("### 📸 Original Image")
    st.image(uploaded_img_path, caption="Uploaded Pipeline Image", use_container_width=True)

    with st.spinner("⏳ Model inferencing, please wait..."):
        result = CLIENT.infer(uploaded_img_path, model_id=MODEL_ID)
        # 兼容两种情况：如果 result 有 json 方法则调用，否则直接当作字典
        if hasattr(result, 'json'):
            predictions_json = result.json()
        else:
            predictions_json = result

    # 读取图像用于绘制
    img = cv2.imread(uploaded_img_path)
    inferenced_img = img.copy()
    collected = []

    for box in predictions_json.get('predictions', []):
        x_center = box['x']
        y_center = box['y']
        width = box['width']
        height = box['height']
        x0 = x_center - width / 2
        x1 = x_center + width / 2
        y0 = y_center - height / 2
        y1 = y_center + height / 2
        class_name = box['class']
        conf = box['confidence']

        start = (int(x0), int(y0))
        end = (int(x1), int(y1))

        if class_name.lower() == 'gas-pipelines':
            color = (255, 255, 0)
            alpha = 0.25
            cv2.putText(inferenced_img, f"{class_name} {conf:.2f}", (int(x0)+5, int(y1)-55),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
        else:
            color = (255, 0, 0)
            alpha = 0.35
            cv2.putText(inferenced_img, f"{class_name} {conf:.2f}", (int(x0)+5, int(y0)-55),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)

        overlay = inferenced_img.copy()
        cv2.rectangle(overlay, start, end, color, -1)
        cv2.addWeighted(overlay, alpha, inferenced_img, 1-alpha, 0, inferenced_img)

        collected.append({
            "Defect Type": class_name,
            "Confidence": f"{conf:.2f}",
            "BBox Coordinates": [int(x0), int(x1), int(y0), int(y1)],
            "Width (px)": int(width),
            "Height (px)": int(height),
            "Area (px²)": abs(int(x0)-int(x1)) * abs(int(y0)-int(y1))
        })

    out_path = "output.jpg"
    cv2.imwrite(out_path, inferenced_img)

    st.session_state.detection_done = True
    st.session_state.predictions_json = predictions_json
    st.session_state.output_image_path = out_path
    st.session_state.input_image_path = uploaded_img_path
    st.session_state.collected_predictions = collected

    st.markdown("### 🔍 Defect Detection Results")
    col_img, col_info = st.columns([2, 1])
    with col_img:
        st.image(out_path, caption="Annotated Result", use_container_width=True)
    with col_info:
        if collected:
            st.success(f"Detected {len(collected)} defect(s)")
            for p in collected:
                st.markdown(f"- **{p['Defect Type']}** (Confidence: {p['Confidence']})")
        else:
            st.info("No defects detected")

    tab1, tab2 = st.tabs(["📋 Data Table", "📄 JSON Format"])
    with tab1:
        st.dataframe(collected, use_container_width=True)
    with tab2:
        st.json(predictions_json)

# ===============================
# PDF 生成函数
# ===============================
def generate_pdf_from_session():
    if not st.session_state.detection_done:
        return None
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Intelligent Pipeline Defect Detection Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Auto Detection Results", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Original Image", ln=True, align='C')
    pdf.image(st.session_state.input_image_path, x=10, y=None, w=160)
    pdf.ln(5)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Annotated Detection Results", ln=True, align='C')
    pdf.image(st.session_state.output_image_path, x=10, y=None, w=160)
    pdf.ln(10)

    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, txt="Detected Defects Details:", ln=True)
    pdf.set_font("Arial", size=9)
    for item in st.session_state.predictions_json.get('predictions', []):
        text = f"Type: {item['class']}, Confidence: {item['confidence']:.2f}, Location: ({item['x']}, {item['y']}), Size: {item['width']}x{item['height']}"
        pdf.multi_cell(0, 8, txt=text)

    pdf.ln(5)
    pdf.set_font("Arial", size=9)
    pdf.cell(0, 10, txt=f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf_output = "detection_report.pdf"
    pdf.output(pdf_output)
    return pdf_output

def display_pdf_download_button(pdf_path):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="detection_report.pdf" style="text-decoration: none; background-color: #1e3c72; color: white; padding: 8px 16px; border-radius: 8px;">📥 Download PDF Report</a>'
        st.markdown(href, unsafe_allow_html=True)

# ===============================
# 主界面布局
# ===============================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/pipeline.png", width=80)
    st.title("🔧 Smart Diagnosis Assistant")
    st.markdown("---")
    st.markdown("### Instructions")
    st.markdown("""
    1. Upload a pipeline image (jpg/png)
    2. Click **'Start Detection'**
    3. View defect locations and types
    4. Export PDF report
    """)
    st.markdown("---")
    st.caption("Built with YOLOv11 + Roboflow | Computer Design Competition Entry")

st.title("🛠️ Pipeline Defect Intelligent Detection System")
st.markdown("> Deep learning based automated pipeline defect recognition tool — Fast, Accurate, Easy-to-use")

with st.form("detection_form", clear_on_submit=False):
    uploaded_file = st.file_uploader("📂 Upload Pipeline Image", type=["png", "jpg", "jpeg"],
                                     help="Supported formats: JPG, PNG. Recommended resolution ≥ 640x480")
    submitted = st.form_submit_button("🚀 Start Detection", use_container_width=True)

if submitted and uploaded_file is not None:
    image = Image.open(uploaded_file)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    byte_io = io.BytesIO()
    image.save(byte_io, format='JPEG')
    temp_input_path = "input.jpg"
    with open(temp_input_path, "wb") as f:
        f.write(byte_io.getvalue())

    run_inference_and_save(temp_input_path)

elif submitted and uploaded_file is None:
    st.warning("⚠️ Please upload an image first.")

if st.session_state.detection_done:
    st.markdown("---")
    if st.button("📄 Generate PDF Report", type="primary"):
        pdf_file = generate_pdf_from_session()
        if pdf_file:
            display_pdf_download_button(pdf_file)
        else:
            st.error("Failed to generate report, please try again.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Computer Design Competition Entry | Intelligent Detection Algorithm Demo</div>", unsafe_allow_html=True)