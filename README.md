# 西安交通大学-青岛五十八中意向生收集系统

## 项目简介

本项目是一个基于 PyQt5 开发的图形化学生信息收集系统，专为西安交通大学与青岛第五十八中学合作的招生意向调查设计。系统提供了友好的用户界面，用于收集学生的基本信息、学业成绩、选考科目以及专业意向等数据，并支持数据导出至 Excel 文件。

## 主要功能

### 1. 欢迎页面
- 显示西安交通大学校徽（通过点阵图形渲染）
- 提供系统使用确认、检查导出和关闭按钮
- 支持查看已收集的学生信息统计

### 2. 信息收集表单
- **基本信息**：姓名、所在中学、联系电话
- **学业信息**：
  - 选考科目（物理、化学、生物、政治、历史、地理）
  - 最近一次考试分数
  - 总分数（默认750分）
  - 最近一次年级排名
- **专业意向**：
  - 按学院分类的专业选择
  - 支持搜索功能（学院-专业）
  - 涵盖西安交通大学26个学院的120+个专业

### 3. 数据管理
- 自动保存学生信息至 `res.xlsx` Excel 文件
- 实时日志记录（存储在 `log/` 目录）
- 数据完整性检查功能
- 支持批量信息收集

### 4. 校徽处理工具（base01.py）
- 将校徽图片转换为 512×512 二值矩阵
- 支持红白色彩识别和转换
- 可视化功能
- 支持批量处理

## 技术栈

- **界面框架**：PyQt5
- **数据处理**：pandas, numpy, openpyxl
- **图像处理**：Pillow
- **日志系统**：loguru
- **其他依赖**：详见 `requirements.txt`

## 安装说明

### 环境要求
- Python 3.7+
- Windows 11 x64

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/BukSeong/enroll_collect.git
cd enroll_collect
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 准备校徽文件（可选）
```bash
# 如果需要重新生成校徽点阵文件
python base01.py
```

## 使用指南

### 启动系统
```bash
python collect.py
```

### 操作流程

1. **启动程序**
   - 运行后会显示欢迎页面
   - 点击"确认使用"进入信息收集界面

2. **填写学生信息**
   - 依次填写各项必填信息
   - 选考科目可多选
   - 点击"选择意向报考专业"按钮打开专业选择对话框

3. **选择专业**
   - 先选择学院，再选择专业
   - 也可以直接在专业下拉框中输入"学院-专业"进行搜索
   - 确认选择后返回表单

4. **提交信息**
   - 点击"提交"按钮保存数据
   - 系统会自动验证信息完整性
   - 提交成功后显示成功页面，可选择继续收集或返回主页

5. **数据导出**
   - 在欢迎页面点击"检查导出"查看已收集的学生信息统计
   - 数据自动保存在 `res.xlsx` 文件中

## 项目结构

```
enroll_collect/
├── collect.py           # 主程序（信息收集系统）
├── base01.py           # 校徽图片处理工具
├── requirements.txt    # Python依赖包
├── xjtulogo.jpg        # 西安交通大学校徽原图
├── logo_matrix.npy     # 校徽点阵数据文件
├── res.xlsx           # 学生信息导出文件（自动生成）
├── log/               # 日志目录（自动生成）
└── README.md          # 项目说明文档
```

## 专业列表

系统包含西安交通大学26个学院的专业，包括：
- 管理学院、经金学院、电气学院、电信学部
- 钱学森学院、医学部、化学学院、机械学院
- 航天学院、能动学院、化工学院、物理学院
- 法学院、材料学院、人居学院、数学学院
- 外语学院、新闻学院、人文学院、公管学院
- 仪器学院、生命学院、联合设计与创新学院
- 马克思主义学院等

详细专业列表请参见 `collect.py` 中的 `major_dict` 字典。

## 日志系统

系统使用 loguru 记录所有操作日志：
- 日志文件存储在 `log/` 目录
- 文件名格式：`YYYYMMDD_HHMMSS.log`
- 支持日志轮转（单文件最大10MB）
- 日志保留10天

## 校徽处理说明

`base01.py` 提供了校徽图片处理功能：

### 单个图片处理
```python
from base01 import convert_logo_to_matrix, visualize_matrix

# 转换校徽为矩阵
matrix = convert_logo_to_matrix("xjtulogo.jpg", "logo_matrix.npy")

# 生成可视化图片
visualize_matrix(matrix, "logo_visualization.png")
```

### 批量处理
```python
from base01 import batch_process_logos

# 批量处理文件夹中的所有校徽图片
batch_process_logos("input_logos", "output_matrices")
```

## 开发说明

### 自定义专业列表
在 `collect.py` 中修改 `major_dict` 字典即可自定义专业列表：

```python
major_dict = {
    "学院名称": ["专业1", "专业2", ...],
    ...
}
```

### 修改默认中学
在 `FormPage` 类的 `init_ui()` 方法中修改：
```python
self.school_input = QLineEdit("你的学校名称")
```

### 调整窗口大小
在 `MainWindow` 类的 `init_ui()` 方法中修改：
```python
self.resize(1920, 1200)  # 宽度, 高度
```

## 注意事项

1. 首次运行前请确保 `logo_matrix.npy` 文件存在，若不存在程序会自动创建默认点阵
2. 系统不会覆盖已有的 `res.xlsx` 文件，而是追加新数据
3. 电话号码字段不做格式限制，可根据需要自行添加验证
4. 建议在正式使用前进行数据备份

## 作者信息

**Author**: BukSeong  
**GitHub**: https://github.com/BukSeong  
**License**: 转载请注明出处 (Please indicate the source when reposting)

## 贡献

欢迎提交 Issue 和 Pull Request 来改进本项目。

## 更新日志

- **v1.0.0** (初始版本)
  - 实现基础信息收集功能
  - 支持专业选择和搜索
  - Excel数据导出
  - 日志记录系统
  - 校徽点阵显示
