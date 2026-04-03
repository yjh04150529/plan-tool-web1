#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鸿耀一生计划书工具 - Vercel 服务器less版本
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import base64
import io

# HTML 模板（内嵌，无需外部文件）
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>鸿耀一生计划书工具</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 10px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1a5276 0%, #2874a6 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 { font-size: 22px; margin-bottom: 5px; }
        .header p { font-size: 14px; opacity: 0.9; }
        .form-section { padding: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label {
            display: block;
            font-size: 14px;
            color: #333;
            margin-bottom: 5px;
            font-weight: 500;
        }
        .form-group label .required { color: #e74c3c; }
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #2874a6;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .presets {
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .presets h3 {
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
        }
        .preset-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .preset-btn {
            padding: 8px 12px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .preset-btn:hover {
            background: #2874a6;
            color: white;
            border-color: #2874a6;
        }
        .btn-primary {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-bottom: 10px;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(46, 204, 113, 0.4);
        }
        .btn-primary:disabled {
            background: #95a5a6;
            cursor: not-allowed;
            transform: none;
        }
        .btn-secondary {
            width: 100%;
            padding: 12px;
            background: white;
            color: #2874a6;
            border: 2px solid #2874a6;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-secondary:hover {
            background: #2874a6;
            color: white;
        }
        .result-section {
            padding: 0 20px 20px;
            display: none;
        }
        .result-section.show { display: block; }
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .result-header h2 { font-size: 18px; color: #333; }
        .summary-cards {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        .summary-card.highlight {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .summary-card .label {
            font-size: 12px;
            opacity: 0.9;
            margin-bottom: 5px;
        }
        .summary-card .value {
            font-size: 18px;
            font-weight: 600;
        }
        .table-container {
            overflow-x: auto;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            background: white;
        }
        th {
            background: #1a5276;
            color: white;
            padding: 10px 8px;
            text-align: center;
            font-weight: 500;
            white-space: nowrap;
        }
        td {
            padding: 10px 8px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }
        tr:nth-child(even) { background: #f8f9fa; }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .loading.show { display: block; }
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #2874a6;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #333;
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 14px;
            opacity: 0;
            transition: all 0.3s;
            z-index: 1000;
        }
        .toast.show {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
        }
        .toast.error { background: #e74c3c; }
        .toast.success { background: #27ae60; }
        @media (max-width: 400px) {
            .form-row { grid-template-columns: 1fr; }
            .summary-cards { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>鸿耀一生（分红型）</h1>
            <p>保险计划书生成工具</p>
        </div>
        <div class="form-section">
            <div class="form-row">
                <div class="form-group">
                    <label><span class="required">*</span> 投保人年龄</label>
                    <select id="age">
                        <option value="18">18岁</option><option value="19">19岁</option><option value="20">20岁</option>
                        <option value="21">21岁</option><option value="22">22岁</option><option value="23">23岁</option>
                        <option value="24">24岁</option><option value="25">25岁</option><option value="26">26岁</option>
                        <option value="27">27岁</option><option value="28">28岁</option><option value="29">29岁</option>
                        <option value="30">30岁</option><option value="31">31岁</option><option value="32">32岁</option>
                        <option value="33">33岁</option><option value="34">34岁</option><option value="35">35岁</option>
                        <option value="36">36岁</option><option value="37">37岁</option><option value="38">38岁</option>
                        <option value="39">39岁</option><option value="40">40岁</option><option value="41">41岁</option>
                        <option value="42">42岁</option><option value="43">43岁</option><option value="44">44岁</option>
                        <option value="45">45岁</option><option value="46">46岁</option><option value="47">47岁</option>
                        <option value="48">48岁</option><option value="49">49岁</option><option value="50">50岁</option>
                        <option value="51">51岁</option><option value="52">52岁</option><option value="53">53岁</option>
                        <option value="54">54岁</option><option value="55">55岁</option><option value="56">56岁</option>
                        <option value="57">57岁</option><option value="58">58岁</option><option value="59" selected>59岁</option>
                        <option value="60">60岁</option><option value="61">61岁</option><option value="62">62岁</option>
                        <option value="63">63岁</option><option value="64">64岁</option><option value="65">65岁</option>
                    </select>
                </div>
                <div class="form-group">
                    <label><span class="required">*</span> 性别</label>
                    <select id="gender">
                        <option value="女" selected>女</option>
                        <option value="男">男</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label><span class="required">*</span> 缴费方式</label>
                    <select id="payment_method">
                        <option value="趸交">趸交</option>
                        <option value="3年">3年</option>
                        <option value="5年" selected>5年</option>
                        <option value="10年">10年</option>
                    </select>
                </div>
                <div class="form-group">
                    <label><span class="required">*</span> 年交保费（元）</label>
                    <input type="number" id="premium" value="60000" placeholder="请输入金额">
                </div>
            </div>
            <div class="form-group">
                <label>客户姓名（可选）</label>
                <input type="text" id="customer_name" placeholder="输入客户姓名">
            </div>
            <div class="presets">
                <h3>⚡ 快速预设方案</h3>
                <div class="preset-buttons">
                    <button class="preset-btn" onclick="applyPreset(59, '女', '5年', 60000)">59岁女-5年-6万</button>
                    <button class="preset-btn" onclick="applyPreset(50, '男', '5年', 100000)">50岁男-5年-10万</button>
                    <button class="preset-btn" onclick="applyPreset(40, '女', '10年', 50000)">40岁女-10年-5万</button>
                    <button class="preset-btn" onclick="applyPreset(35, '男', '3年', 200000)">35岁男-3年-20万</button>
                    <button class="preset-btn" onclick="applyPreset(60, '女', '趸交', 300000)">60岁女-趸交-30万</button>
                </div>
            </div>
            <button class="btn-primary" onclick="generatePlan()" id="generateBtn">📝 生成计划书</button>
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>正在计算...</p>
            </div>
        </div>
        <div class="result-section" id="resultSection">
            <div class="result-header">
                <h2>📊 计划书预览</h2>
            </div>
            <div class="summary-cards">
                <div class="summary-card">
                    <div class="label">累计保费</div>
                    <div class="value" id="totalPremium">-</div>
                </div>
                <div class="summary-card highlight">
                    <div class="label">第10年现金价值</div>
                    <div class="value" id="year10Value">-</div>
                </div>
            </div>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>年度</th><th>年龄</th><th>年交保费</th><th>累计保费</th>
                            <th>现金价值</th><th>当年红利</th><th>生存总利益</th>
                        </tr>
                    </thead>
                    <tbody id="resultTable"></tbody>
                </table>
            </div>
            <button class="btn-secondary" onclick="exportExcel()" style="margin-top: 15px;">📥 导出 Excel</button>
        </div>
    </div>
    <div class="toast" id="toast"></div>
    <script>
        let currentData = null;
        function showToast(message, type = 'info') {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast show ' + type;
            setTimeout(() => toast.classList.remove('show'), 3000);
        }
        function applyPreset(age, gender, payment, premium) {
            document.getElementById('age').value = age;
            document.getElementById('gender').value = gender;
            document.getElementById('payment_method').value = payment;
            document.getElementById('premium').value = premium;
            showToast('已应用: ' + age + '岁' + gender + ' ' + payment + '交', 'success');
        }
        async function generatePlan() {
            const age = parseInt(document.getElementById('age').value);
            const gender = document.getElementById('gender').value;
            const payment_method = document.getElementById('payment_method').value;
            const premium = parseFloat(document.getElementById('premium').value);
            if (!age || !premium) {
                showToast('请填写完整信息', 'error');
                return;
            }
            document.getElementById('generateBtn').disabled = true;
            document.getElementById('loading').classList.add('show');
            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ age, gender, payment_method, premium })
                });
                const result = await response.json();
                if (result.success) {
                    currentData = result.data;
                    displayResults(result.data);
                    showToast('计划书生成成功！', 'success');
                } else {
                    showToast(result.error || '生成失败', 'error');
                }
            } catch (error) {
                showToast('网络错误，请重试', 'error');
            } finally {
                document.getElementById('generateBtn').disabled = false;
                document.getElementById('loading').classList.remove('show');
            }
        }
        function displayResults(data) {
            const resultSection = document.getElementById('resultSection');
            const year10Record = data[9] || data[data.length - 1];
            const lastRecord = data[data.length - 1];
            document.getElementById('totalPremium').textContent = '¥' + Math.round(lastRecord['累计保费']).toLocaleString();
            document.getElementById('year10Value').textContent = '¥' + Math.round(year10Record['现金价值']).toLocaleString();
            let html = '';
            const displayData = [...data.slice(0, 20)];
            if (data.length > 25) {
                html += '<tr><td colspan="7" style="color:#999;">...</td></tr>';
                displayData.push(...data.slice(-5));
            } else {
                displayData.push(...data.slice(20));
            }
            displayData.forEach(row => {
                html += '<tr><td>' + row['保单年度'] + '</td><td>' + row['年龄'] + '</td>' +
                    '<td>¥' + Math.round(row['年交保费']).toLocaleString() + '</td>' +
                    '<td>¥' + Math.round(row['累计保费']).toLocaleString() + '</td>' +
                    '<td>¥' + Math.round(row['现金价值']).toLocaleString() + '</td>' +
                    '<td>¥' + Math.round(row['当年红利']).toLocaleString() + '</td>' +
                    '<td><strong>¥' + Math.round(row['生存总利益']).toLocaleString() + '</strong></td></tr>';
            });
            document.getElementById('resultTable').innerHTML = html;
            resultSection.classList.add('show');
            resultSection.scrollIntoView({ behavior: 'smooth' });
        }
        async function exportExcel() {
            if (!currentData) {
                showToast('请先生成计划书', 'error');
                return;
            }
            const info = {
                name: document.getElementById('customer_name').value || '客户',
                age: document.getElementById('age').value,
                gender: document.getElementById('gender').value,
                payment_method: document.getElementById('payment_method').value,
                premium: parseFloat(document.getElementById('premium').value)
            };
            try {
                const response = await fetch('/api/export-excel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: currentData, info: info })
                });
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = '鸿耀一生计划书_' + info.name + '_' + new Date().toISOString().slice(0,10).replace(/-/g,'') + '.xlsx';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    showToast('Excel导出成功！', 'success');
                } else {
                    showToast('导出失败', 'error');
                }
            } catch (error) {
                showToast('导出错误', 'error');
            }
        }
    </script>
</body>
</html>'''

def calculate_plan(age, gender, payment_method, premium):
    """计算保险计划书数据"""
    if payment_method == "趸交":
        pay_years = 1
    else:
        pay_years = int(payment_method.replace("年", ""))
    
    total_years = min(105 - age, 45)
    data = []
    gender_factor = 1.02 if gender == "男" else 1.0
    
    for year in range(1, total_years + 1):
        current_age = age + year - 1
        
        if year <= pay_years:
            annual_premium = premium
            total_premium = premium * year
        else:
            annual_premium = 0
            total_premium = premium * pay_years
        
        if year <= pay_years:
            cash_value = total_premium * (0.35 + 0.08 * year) * gender_factor
        else:
            years_after = year - pay_years
            cash_value = total_premium * (0.8 + 0.008 * years_after) * gender_factor
        
        death_benefit = max(total_premium * 1.2, cash_value * 1.15)
        annual_bonus = cash_value * 0.018 if year > 1 else 0
        total_bonus = sum([d.get("当年红利", 0) for d in data]) + annual_bonus
        total_benefit = cash_value + total_bonus
        
        data.append({
            "保单年度": year,
            "年龄": current_age,
            "年交保费": round(annual_premium, 2),
            "累计保费": round(total_premium, 2),
            "身故/全残保险金": round(death_benefit, 2),
            "现金价值": round(cash_value, 2),
            "当年红利": round(annual_bonus, 2),
            "累计红利": round(total_bonus, 2),
            "生存总利益": round(total_benefit, 2)
        })
    
    return {"data": data}

def create_excel(data, info):
    """创建 Excel 文件（简化版，使用 CSV 格式）"""
    import csv
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 标题
    writer.writerow(["鸿耀一生（分红型）保险计划书"])
    writer.writerow([])
    writer.writerow(["客户姓名:", info.get('name', ''), "投保年龄:", str(info.get('age', '')) + "岁", 
                     "性别:", info.get('gender', ''), "导出日期:", datetime.now().strftime('%Y年%m月%d日')])
    writer.writerow(["缴费方式:", info.get('payment_method', '') + "交", "年交保费:", str(info.get('premium', '')) + "元"])
    writer.writerow([])
    
    # 表头
    headers = ["保单年度", "年龄", "年交保费", "累计保费", "身故/全残保险金", 
               "现金价值", "当年红利", "累计红利", "生存总利益"]
    writer.writerow(headers)
    
    # 数据
    for row in data:
        writer.writerow([
            row["保单年度"],
            row["年龄"],
            row["年交保费"],
            row["累计保费"],
            row["身故/全残保险金"],
            row["现金价值"],
            row["当年红利"],
            row["累计红利"],
            row["生存总利益"]
        ])
    
    return output.getvalue().encode('utf-8-sig')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
    
    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            path = urlparse(self.path).path
            
            if path == '/api/calculate':
                age = int(data.get('age', 0))
                gender = data.get('gender', '女')
                payment_method = data.get('payment_method', '5年')
                premium = float(data.get('premium', 0))
                
                if age < 18 or age > 65:
                    result = {"success": False, "error": "投保人年龄应在18-65岁之间"}
                elif premium <= 0:
                    result = {"success": False, "error": "年交保费必须大于0"}
                else:
                    result = calculate_plan(age, gender, payment_method, premium)
                    result["success"] = True
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            
            elif path == '/api/export-excel':
                from datetime import datetime
                plan_data = data.get('data', [])
                customer_info = data.get('info', {})
                
                excel_data = create_excel(plan_data, customer_info)
                
                filename = f"鸿耀一生计划书_{customer_info.get('name', '客户')}_{datetime.now().strftime('%Y%m%d')}.csv"
                
                self.send_response(200)
                self.send_header('Content-type', 'text/csv; charset=utf-8-sig')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()
                self.wfile.write(excel_data)
            
            else:
                self.send_response(404)
                self.end_headers()
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
    
    def log_message(self, format, *args):
        """禁用默认日志"""
        pass

# Vercel 入口
def handler(event, context):
    """Vercel serverless 处理函数"""
    from http.server import BaseHTTPRequestHandler
    from io import BytesIO
    
    class RequestHandler(BaseHTTPRequestHandler):
        def __init__(self, request_text):
            self.rfile = BytesIO(request_text)
            self.raw_requestline = self.rfile.readline()
            self.error_code = None
            self.error_message = None
            
        def send_error(self, code, message=None):
            self.error_code = code
            self.error_message = message
    
    # 简化的响应处理
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html; charset=utf-8'},
            'body': HTML_TEMPLATE
        }
    
    elif method == 'POST' and path == '/api/calculate':
        try:
            body = json.loads(event.get('body', '{}'))
            age = int(body.get('age', 0))
            gender = body.get('gender', '女')
            payment_method = body.get('payment_method', '5年')
            premium = float(body.get('premium', 0))
            
            if age < 18 or age > 65:
                return {'statusCode': 400, 'body': json.dumps({"success": False, "error": "年龄应在18-65岁之间"})}
            if premium <= 0:
                return {'statusCode': 400, 'body': json.dumps({"success": False, "error": "保费必须大于0"})}
            
            result = calculate_plan(age, gender, payment_method, premium)
            result["success"] = True
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(result)}
        except Exception as e:
            return {'statusCode': 500, 'body': json.dumps({"success": False, "error": str(e)})}
    
    return {'statusCode': 404, 'body': 'Not Found'}
