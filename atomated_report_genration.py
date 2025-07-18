# ===== IMPORT NECESSARY LIBRARIES =====
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import ceil
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

# === CONFIG ===
CSV_FILE = "F:\Sem 5\Intership\Task 2\mobile_phone_sales_data.csv"
PDF_FILE = "F:\Sem 5\Intership\Task 2\mobile_phone_sales_report.pdf"
CHART1 = "top_brands.png"
CHART2 = "avg_price_brand.png"
CHART3 = "ram_vs_storage_heatmap.png"
CHART4 = "price_distribution.png"
CHART5 = "phones_by_year.png"
LOGO_FILE = "logo_placeholder.png"

# === LOAD DATA ===
df = pd.read_csv(CSV_FILE)

# === CLEAN AND EXTRACT ===
if 'Brand' not in df.columns:
    df['Brand'] = df['Variant'].apply(lambda x: str(x).split()[0])

# === CALCULATE INSIGHTS ===
total_phones = len(df)
avg_price = df['Price'].mean()
most_common_brand = df['Brand'].mode()[0]
most_common_color = df['Color'].mode()[0]

# === CHART 1: Top Brands ===
top_brands = df['Brand'].value_counts().nlargest(10)
plt.figure(figsize=(6, 4))
top_brands.plot(kind='bar', color='orange')
plt.title("Top 10 Mobile Brands")
plt.ylabel("Number of Phones Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(CHART1)
plt.close()

# === CHART 2: Avg Price by Brand ===
avg_price_brand = df.groupby("Brand")["Price"].mean().dropna().sort_values(ascending=False).head(10)
plt.figure(figsize=(6, 4))
avg_price_brand.plot(kind='bar', color='red')
plt.title("Average Price by Brand (Top 10)")
plt.ylabel("Avg Price (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(CHART2)
plt.close()

# === CHART 3: Heatmap (RAM vs Storage) ===
heatmap_df = pd.crosstab(df['RAM'], df['Storage'])
plt.figure(figsize=(8, 4))
sns.heatmap(heatmap_df, annot=True, fmt='d', cmap='Blues')
plt.title('RAM vs Storage Availability')
plt.tight_layout()
plt.savefig(CHART3)
plt.close()

# === CHART 4: Price Distribution ===
plt.figure(figsize=(6, 4))
plt.hist(df['Price'], bins=30, color='darkblue', edgecolor='lightblue')
plt.title("Price Distribution")
plt.xlabel("Price (₹)")
plt.ylabel("Number of Phones")
plt.tight_layout()
plt.savefig(CHART4)
plt.close()

# === CHART 5: Phones by Manufacturing Year ===
year_counts = df['Year'].value_counts().sort_index()
plt.figure(figsize=(8, 4))
year_counts.plot(kind='bar', color='mediumseagreen')
plt.title("Phones by Year of Manufacturing")
plt.xlabel("Year")
plt.ylabel("Number of Phones")
plt.tight_layout()
plt.savefig(CHART5)
plt.close()

# === CREATE PLACEHOLDER LOGO ===
plt.figure(figsize=(2, 1))
plt.text(0.5, 0.5, 'Mobile Sales Report', fontsize=20, ha='center', va='center')
plt.axis('off')
plt.savefig(LOGO_FILE, bbox_inches='tight', transparent=True)
plt.close()

# === PDF SETUP ===
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(PDF_FILE, pagesize=A4)
elements = []

# === COVER PAGE ===
elements.append(Image(LOGO_FILE, width=150, height=50))
elements.append(Spacer(1, 20))
elements.append(Paragraph("<u>MOBILE PHONE SALES ANALYSIS REPORT</u>", styles['Title']))
elements.append(Spacer(1, 20))
elements.append(Paragraph("This report presents a comprehensive analysis of mobile phone sales data. The dataset includes various phone models, brands, storage/RAM configurations, and pricing across different regions and years.", styles['Normal']))
elements.append(PageBreak())

# === INSIGHTS SECTION ===
elements.append(Paragraph("📊 Key Sales Insights", styles['Heading1']))
elements.append(Spacer(1, 12))
elements.append(Paragraph(f"<b>Total Phones:</b> {total_phones}", styles['Normal']))
elements.append(Paragraph(f"<b>Average Price:</b> ₹ {avg_price:.2f}", styles['Normal']))
elements.append(Paragraph(f"<b>Most Common Brand:</b> {most_common_brand}", styles['Normal']))
elements.append(Paragraph(f"<b>Most Popular Color:</b> {most_common_color}", styles['Normal']))
elements.append(Spacer(1, 12))

# === INSERT CHARTS ===
elements.append(Image(CHART1, width=400, height=250))
elements.append(Spacer(1, 12))
elements.append(Image(CHART2, width=400, height=250))
elements.append(PageBreak())
elements.append(Image(CHART3, width=400, height=200))
elements.append(Spacer(1, 12))
elements.append(Image(CHART4, width=400, height=250))
elements.append(Spacer(1, 12))
elements.append(Image(CHART5, width=400, height=250))
elements.append(PageBreak())

# === FULL DATA TABLE ===
columns_to_include = ['Brand', 'Variant', 'Color', 'RAM', 'Storage', 'Price', 'Year', 'Location']
full_df = df[columns_to_include].dropna()
rows_per_page = 40
total_pages = ceil(len(full_df) / rows_per_page)

for page in range(total_pages):
    chunk = full_df.iloc[page * rows_per_page:(page + 1) * rows_per_page]
    table_data = [chunk.columns.tolist()] + chunk.values.tolist()

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    elements.append(Paragraph(f"📄 Full Data Table - Page {page + 1}", styles['Heading2']))
    elements.append(table)
    elements.append(PageBreak())

# === PAGE NUMBER FUNCTION ===
def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(200 * mm, 10 * mm, f"Page {page_num}")

# === BUILD PDF ===
doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

print(f"✅ Mobile phone sales report generated: {PDF_FILE}")
