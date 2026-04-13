# PipeDetect：基于YOLOv11的管道缺陷智能检测系统

> 一键上传管道图像，自动识别缺陷位置与类别 —— 专为工业巡检设计的轻量级Web检测工具

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-00FFFF?logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 项目简介

**PipeDetect** 是一套面向管道巡检场景的智能缺陷检测系统，融合了 **YOLOv11** 实时目标检测算法与 **Streamlit** 交互式前端框架。用户无需安装任何专业软件，只需通过浏览器上传管道图像，即可在数秒内获得缺陷位置、类别及置信度的可视化检测结果。

该系统旨在解决传统人工巡检效率低、主观性强、难以覆盖长距离管网等问题，为基础设施维护人员提供即用型 AI 辅助诊断工具。

---

## ✨ 核心功能

- 📤 **图像上传**：支持 JPG、PNG 格式的管道图片，单张图像快速分析
- 🔍 **缺陷检测**：自动识别以下三类常见缺陷：
  - **腐蚀**（Corrosion）
  - **弯曲变形**（Bending）
  - **结构形变**（Deformation）
- 🖍️ **结果可视化**：在原图上绘制彩色半透明边界框，标注缺陷类别与置信度
- 📊 **多维数据展示**：提供检测结果的表格视图、JSON 原始数据及 PDF 报告下载
- 🌐 **跨平台访问**：纯 Web 实现，适配 PC、平板、手机等任何带浏览器的设备

---

## 🛠️ 技术架构

| 模块 | 技术选型 | 说明 |
|------|----------|------|
| 前端界面 | Streamlit | 响应式 UI，无需编写 HTML/CSS/JS |
| 目标检测模型 | YOLOv11 (Ultralytics) | 高性能实时检测，mAP > 92% |
| 推理后端 | Roboflow Inference SDK | 云端 API 调用，单图推理 < 3 秒 |
| 图像处理 | OpenCV + Pillow | 图像读写、边界框绘制、格式转换 |
| 报告生成 | FPDF2 | 生成结构化 PDF 检测报告 |
| 部署方式 | Streamlit Cloud / 本地运行 | 开箱即用，无需额外配置 |

---

## 📦 安装与运行

### 环境要求
- Python 3.9 或更高版本
- 网络连接（用于调用 Roboflow API）

### 1. 克隆仓库
```bash
git clone https://github.com/daanaea/pipes-defect-detection.git
cd pipes-defect-detection
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```
主要依赖包：
- streamlit >= 1.28.0
- opencv-python >= 4.8.0
- pillow >= 10.0.0
- fpdf2 >= 2.7.0
- inference-sdk >= 0.10.0

### 3. 配置 API Key（可选）
若需使用自己的 Roboflow 模型，请在 `Home.py` 中替换以下变量：
```python
API_KEY = "你的API_Key"
MODEL_ID = "你的模型ID"
```
若不修改，系统将使用公开演示模型（有限额，仅供测试）。

### 4. 启动应用
```bash
streamlit run Home.py
```
终端将显示本地访问地址（如 `http://localhost:8501`），在浏览器中打开即可使用。

---

## 🖥️ 使用指南

1. **上传图像**：点击“Browse files”选择一张管道照片（建议分辨率 ≥ 640×480）。
2. **开始检测**：点击“🚀 Start Detection”按钮，系统自动调用模型推理。
3. **查看结果**：
   - 左侧显示标注后的图像
   - 右侧列出检测到的缺陷列表
   - 下方提供数据表格和 JSON 原始数据标签页
4. **导出报告**：点击“📄 Generate PDF Report”下载检测报告（包含原始图、标注图及缺陷详情）。

---

## 📂 项目结构

```
pipes-defect-detection/
├── Home.py               # 主程序入口（Streamlit 应用）
├── requirements.txt      # Python 依赖清单
├── README.md             # 项目说明文档
├── LICENSE               # MIT 许可证
└── output.jpg            # 临时输出图像（运行后生成）
```

---

## 🧪 测试结果

- **数据集**：基于 Roboflow Universe 公开数据集（8448 张标注管道图像）
- **模型指标**：mAP（平均精度均值）达到 **92.3%**
- **实地验证**：在哈萨克斯坦阿拉木图市地上管道网络采集的现场图像上测试，缺陷识别准确率超过 **92%**
- **推理速度**：单张 1280×720 图像平均耗时 **2.8 秒**（含网络延迟）

---

## 🔮 未来规划

- 🎥 增加实时视频流检测（支持无人机/监控摄像头输入）
- 📱 优化移动端界面，适配现场巡检人员
- 🧠 引入缺陷严重程度分级（轻度/中度/重度）
- 🌍 离线部署支持（NVIDIA Jetson 边缘设备）
- 🔌 开放 REST API，便于集成到现有物联网监测平台

---

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request 参与项目改进。如有疑问，请通过以下方式联系：

- **项目主页**：[GitHub 仓库地址](https://github.com/daanaea/pipes-defect-detection)
- **开源协议**：MIT（详见 [LICENSE](./LICENSE) 文件）

---

## 📄 许可证

本项目采用 **MIT 许可证**开源，允许自由使用、修改和分发，但须保留原始版权声明。

---

*PipeDetect —— 让管道巡检更智能、更高效。*