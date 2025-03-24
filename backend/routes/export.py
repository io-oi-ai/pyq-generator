from flask import Blueprint, send_file
import pandas as pd # type: ignore
import io
from services.database import DatabaseService

export_bp = Blueprint('export', __name__)
db = DatabaseService()

@export_bp.route('/export/generations')
def export_generations():
    """导出生成记录为Excel"""
    df = pd.DataFrame(db.get_all_generations())
    
    # 创建内存中的Excel文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Generations')
    
    output.seek(0)
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='generations.xlsx'
    ) 