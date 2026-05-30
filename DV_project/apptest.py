import dash
from dash import html

# Khởi tạo app và bật tính năng đa trang (use_pages=True)
app = dash.Dash(__name__, use_pages=True)

# Layout vỏ rỗng chỉ để test trang của Trọng
app.layout = html.Div([
    html.H1("Môi trường Test cục bộ của Trọng", style={'textAlign': 'center', 'color': 'red'}),
    html.Hr(),
    # Đây là nơi Dash tự động nhúng nội dung file pages/upsets.py vào
    dash.page_container 
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)