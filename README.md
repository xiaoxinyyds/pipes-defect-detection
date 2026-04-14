```markdown
# PipeDetect：管道缺陷智能检测系统

> 基于 YOLOv11 + Streamlit 的轻量级管道缺陷检测工具  
> 上传图像，自动识别腐蚀、弯曲、形变等缺陷，支持 PDF 报告导出

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-00FFFF?logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 项目简介

PipeDetect 是一套面向工业管道巡检场景的智能缺陷检测系统，融合了 **YOLOv11** 实时目标检测算法与 **Streamlit** 交互式前端框架。用户无需安装任何专业软件，只需通过浏览器上传管道图像，即可在数秒内获得缺陷位置、类别及置信度的可视化检测结果。

本系统旨在解决传统人工巡检效率低、主观性强、难以覆盖长距离管网等问题，为基础设施维护人员提供即用型 AI 辅助诊断工具。

---

## ✨ 核心功能

- 📤 **图像上传**：支持 JPG、PNG 格式的管道图片
- 🔍 **缺陷检测**：自动识别 **腐蚀（Corrosion）**、**弯曲（Bending）**、**形变（Deformation）** 等常见缺陷
- 🖍️ **结果可视化**：在原图上绘制彩色半透明边界框，标注类别与置信度
- 📊 **多维展示**：提供检测结果表格、JSON 原始数据及 PDF 报告下载
- 🌐 **跨平台访问**：纯 Web 实现，适配 PC、平板、手机等设备

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
git clone https://github.com/xiaoxinyyds/pipes-defect-detection.git
cd pipes-defect-detection
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 API Key（可选）
系统默认使用公开演示 API Key，可直接运行。  
如需使用自己的 Roboflow 模型，请编辑 `Home.py`，替换以下变量：
```python
API_KEY = "你的API_Key"
MODEL_ID = "你的模型ID"
```

### 4. 启动应用
```bash
streamlit run Home.py
```
在浏览器中打开 `http://localhost:8501` 即可使用。

---

## 🖥️ 使用指南

1. 点击 “Browse files” 上传管道图像（建议分辨率 ≥ 640×480）。
2. 点击 “🚀 Start Detection” 开始检测。
3. 查看标注结果、缺陷列表及置信度。
4. 点击 “📄 Generate PDF Report” 下载检测报告。

---

## 📂 项目结构

```
pipes-defect-detection/
├── Home.py               # 主程序入口
├── requirements.txt      # Python 依赖
├── README.md             # 项目说明
├── LICENSE               # MIT 许可证
└── output.jpg            # 临时输出图像（运行后生成）
```

---

## 🧪 测试结果

- **数据集**：基于 Roboflow Universe 公开管道数据集（8448 张标注图像）
- **模型指标**：mAP（平均精度均值）达 **92.3%**
- **实地验证**：在真实管道现场图像上测试，缺陷识别准确率超过 **92%**
- **推理速度**：单张 1280×720 图像平均耗时 **2.8 秒**

---

## 🔮 未来规划

- 🎥 增加实时视频流检测（支持无人机/监控摄像头）
- 📱 优化移动端界面，适配现场巡检
- 🧠 引入缺陷严重程度分级（轻度/中度/重度）
- 🌍 离线部署支持（NVIDIA Jetson 边缘设备）
- 🔌 开放 REST API，便于集成到物联网平台

---

## 🤝 贡献与反馈

欢迎提交 Issue 或 Pull Request。  
项目地址：[https://github.com/xiaoxinyyds/pipes-defect-detection](https://github.com/xiaoxinyyds/pipes-defect-detection)

---

## 📄 许可证

本项目采用 **MIT 许可证**，详见 [LICENSE](./LICENSE) 文件。

---

*PipeDetect —— 让管道巡检更智能、更高效。*
