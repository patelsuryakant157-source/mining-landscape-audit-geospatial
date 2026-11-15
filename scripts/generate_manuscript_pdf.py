import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

pdf_filename = "Dhanpuri_Amlai_Ecological_Audit_Manuscript.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    leftMargin=46,
    rightMargin=46,
    topMargin=46,
    bottomMargin=46
)

styles = getSampleStyleSheet()

# Custom Editorial Typography
title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=17,
    leading=22,
    textColor=colors.HexColor('#111827'),
    alignment=0,
    spaceAfter=10
)

meta_style = ParagraphStyle(
    'DocMeta',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor('#4B5563'),
    spaceAfter=12
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=16,
    textColor=colors.HexColor('#0F172A'),
    spaceBefore=14,
    spaceAfter=6,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=10,
    spaceAfter=4,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyDark',
    parent=styles['Normal'],
    fontName='Times-Roman',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#1F2937'),
    spaceAfter=6
)

abstract_style = ParagraphStyle(
    'AbstractBlock',
    parent=styles['Normal'],
    fontName='Times-Italic',
    fontSize=8.5,
    leading=12.5,
    textColor=colors.HexColor('#334155'),
    leftIndent=15,
    rightIndent=15,
    spaceAfter=12
)

tbl_cell_style = ParagraphStyle(
    'TblCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.5,
    leading=10,
    textColor=colors.HexColor('#1F2937'),
    alignment=1
)

tbl_hdr_style = ParagraphStyle(
    'TblHdr',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=11,
    textColor=colors.white,
    alignment=1
)

caption_style = ParagraphStyle(
    'FigureCaption',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=8,
    leading=11,
    textColor=colors.HexColor('#475569'),
    alignment=1,
    spaceBefore=4,
    spaceAfter=10
)

story = []

# Title & Metadata
story.append(Paragraph("Long-Term (2001–2024) Spatiotemporal Audit of Coal Extraction, Landscape Fragmentation, and Riparian Encroachment in the Dhanpuri–Amlai Coalfield Complex, Central India", title_style))
story.append(Paragraph("<b>Target Venue:</b> Environmental Monitoring and Assessment / Remote Sensing Applications: Society and Environment<br/><b>Keywords:</b> Surface Mining, Dhanpuri OCM, Landscape Ecology, PyLandStats, Riparian Buffer, Google Earth Engine, Son River Basin", meta_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))

# Abstract
story.append(Paragraph("<b>Abstract:</b> Open-cast coal extraction in Central India’s Gondwana coalfields drives extensive land use/land cover (LULC) transformation, ecosystem fragmentation, and hydrologic stress. This study evaluates a 23-year environmental trajectory (2001–2024) across the Dhanpuri–Amlai coalfield complex in the Shahdol district, Madhya Pradesh, utilizing multi-temporal Landsat 7 ETM+ and Landsat 8 OLI observations processed via Google Earth Engine (GEE). To resolve historical classification artifacts caused by high-albedo post-harvest fallow soils and dry riverbeds, a multi-index architecture combining the Normalized Difference Vegetation Index (NDVI), the Modified Normalized Difference Water Index (MNDWI), and Shortwave Infrared (SWIR) spectral brightness constraints was deployed. Structural landscape metrics were quantified using PyLandStats, and zonal extraction encroachment was audited across 1 km, 2 km, and 5 km riparian buffers flanking the Son River corridor. Classification performance reached an Overall Accuracy of 88.33% (κ = 0.8444), with a 100.00% User’s Accuracy for active mining cuts. Active excavation footprints contracted from a dispersed baseline of 1,924.38 ha (8.59% of the landscape across 1,799 patches) to a consolidated, deepened core of 269.46 ha (1.20% across 279 patches). Concurrently, core vegetative canopies expanded from 2,303.01 ha to 11,664.18 ha, driven by aggressive biological reclamation over backfilled legacy spoils and plantation maturation. Active mining within the Son River’s critical 1 km riparian corridor declined by 71.26% (-214.56 ha), yet 86.51 ha remains within this primary discharge buffer. These findings demonstrate spatial consolidation alongside an ongoing need for continuous point-source runoff management along the Son River.", abstract_style))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E2E8F0'), spaceAfter=10))

# Section 1: Introduction
story.append(Paragraph("1. Introduction", h1_style))
story.append(Paragraph("The Dhanpuri–Amlai coal complex, operated by South Eastern Coalfields Limited (SECL) within the Sohagpur Coalfield basin, constitutes one of Madhya Pradesh's primary opencast energy-extraction hubs. While opencast mining provides critical thermal fuel supplies, the mechanical removal of overburden, open-pit dewatering, and spoil dumping disrupt regional hydrological regimes and natural Sal (<i>Shorea robusta</i>) forest corridors.", body_style))
story.append(Paragraph("A major analytical challenge in historical remote-sensing audits across Central India is the spectral confusion between dry fallow agricultural fields, exposed river sands, and carbonaceous mine pit surfaces when using single-band vegetation thresholds. In dry post-monsoon or pre-monsoon windows, exposed dry soils present low vegetative signals that mirror barren overburden. Furthermore, the proximity of active mining faces to perennial drainage systems—specifically the Son River—presents long-term risks of sedimentation, trace-metal mobilization, and riparian habitat degradation.", body_style))
story.append(Paragraph("This investigation provides an empirical, multi-decadal landscape audit of the Dhanpuri–Amlai complex. The primary objectives are to: (1) Develop a calibrated spectral classification model that eliminates bare-soil false positives across multi-sensor platforms (Landsat 7 vs. Landsat 8); (2) Measure patch-level structural fragmentation dynamics using FRAGSTATS-compliant landscape spatial metrics; (3) Quantify open-cast encroachment across concentric riparian buffer bands along the Son River; and (4) Provide a statistically validated confusion matrix verifying thematic accuracy.", body_style))

# Section 2: Materials & Methods
story.append(Paragraph("2. Materials and Methods", h1_style))
story.append(Paragraph("<b>2.1 Study Area</b><br/>The Region of Interest (ROI) spans an area of approximately 204.6 km² in the Shahdol district of Madhya Pradesh, bound by 81.50°E to 81.65°E and 23.10°N to 23.22°N. The domain encompasses the Dhanpuri Open Cast Mine (OCM), the Amlai industrial/railway siding corridor, extensive agricultural matrices, secondary deciduous forest remnants, and the meandering trunk stream of the Son River in the northern sector.", body_style))
story.append(Paragraph("<b>2.2 Satellite Preprocessing & Spectral Filtering</b><br/>Tier 1, Level-2 Surface Reflectance products were accessed via Google Earth Engine: Landsat 7 ETM+ (2000–2002) and Landsat 8 OLI (2023–2024). Surfaces were normalized using NDVI, MNDWI, and SWIR bands. True mining surfaces absorb heavily in both red and SWIR spectra (ρ < 0.15 and ρ < 0.20), cleanly rejecting high-albedo dry sands and fallow soils into the rural matrix.", body_style))

# Section 3: Results
story.append(Paragraph("3. Results and Environmental Discussion", h1_style))
story.append(Paragraph("<b>3.1 Landscape Fragmentation Dynamics</b>", h2_style))

# Insert Calibrated Comparison Map
map_path1 = "dhanpuri_calibrated_comparison.png"
if os.path.exists(map_path1):
    story.append(Image(map_path1, width=7.0*inch, height=3.5*inch))
    story.append(Paragraph("<b>Figure 1:</b> Calibrated multi-temporal landscape classification of Dhanpuri–Amlai coalfield (2001 Baseline vs. 2024 Extent) isolating active pits, canopy, buffer, and water bodies.", caption_style))

# Table 1: PyLandStats
pyland_data = [
    [Paragraph("Class Name", tbl_hdr_style), Paragraph("Year", tbl_hdr_style), Paragraph("Area (ha)", tbl_hdr_style), Paragraph("PLAND (%)", tbl_hdr_style), Paragraph("Patch Count", tbl_hdr_style), Paragraph("Mean Area (ha)", tbl_hdr_style), Paragraph("Edge Dens (m/ha)", tbl_hdr_style)],
    [Paragraph("Active Pit / Overburden", tbl_cell_style), "2001", "1,924.38", "8.59", "1,799", "1.07", "38.94"],
    ["", "2024", "269.46", "1.20", "279", "0.97", "5.63"],
    [Paragraph("Core Forest Canopy", tbl_cell_style), "2001", "2,303.01", "10.28", "1,521", "1.51", "36.53"],
    ["", "2024", "11,664.18", "52.08", "1,236", "9.44", "95.81"],
    [Paragraph("Matrix / Cultivated Buffer", tbl_cell_style), "2001", "17,947.89", "80.13", "279", "64.33", "74.48"],
    ["", "2024", "10,078.65", "45.00", "1,655", "6.09", "101.99"],
    [Paragraph("Son River / Mine Sump", tbl_cell_style), "2001", "222.84", "0.99", "180", "1.24", "3.57"],
    ["", "2024", "385.83", "1.72", "208", "1.85", "4.75"]
]
t1 = Table(pyland_data, colWidths=[1.8*inch, 0.6*inch, 0.9*inch, 0.8*inch, 0.9*inch, 1.0*inch, 1.0*inch])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BACKGROUND', (0,1), (-1,2), colors.HexColor('#F8FAFC')),
    ('BACKGROUND', (0,3), (-1,4), colors.HexColor('#FFFFFF')),
    ('BACKGROUND', (0,5), (-1,6), colors.HexColor('#F8FAFC')),
    ('BACKGROUND', (0,7), (-1,8), colors.HexColor('#FFFFFF')),
]))
story.append(t1)
story.append(Paragraph("<b>Table 1:</b> Landscape structural metrics computed via PyLandStats for 2001 and 2024.", caption_style))

story.append(Spacer(1, 8))
story.append(Paragraph("<b>3.2 Son River Riparian Corridor Encroachment</b>", h2_style))

# Insert Buffer Map
map_path2 = "son_river_buffer_audit.png"
if os.path.exists(map_path2):
    story.append(Image(map_path2, width=7.0*inch, height=3.5*inch))
    story.append(Paragraph("<b>Figure 2:</b> Concentric riparian buffers (1 km, 2 km, 5 km) along the Son River channel tracing spatial mining shifts.", caption_style))

# Table 2: Riparian Encroachment
buffer_data = [
    [Paragraph("Riparian Buffer Zone", tbl_hdr_style), Paragraph("2001 Mining (ha)", tbl_hdr_style), Paragraph("2024 Mining (ha)", tbl_hdr_style), Paragraph("Net Change (ha)", tbl_hdr_style), Paragraph("Relative Change (%)", tbl_hdr_style)],
    [Paragraph("1 km Buffer (Critical Riparian)", tbl_cell_style), "301.08", "86.51", "-214.56", "-71.26%"],
    [Paragraph("2 km Buffer (Hydrological Zone)", tbl_cell_style), "97.20", "12.42", "-84.78", "-87.22%"],
    [Paragraph("5 km Buffer (Macro Catchment)", tbl_cell_style), "131.58", "15.98", "-115.60", "-87.86%"],
    [Paragraph("<b>Total Catchment Disturbance</b>", tbl_cell_style), "<b>529.86</b>", "<b>114.91</b>", "<b>-414.95</b>", "<b>-78.31%</b>"]
]
t2 = Table(buffer_data, colWidths=[2.6*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.1*inch])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F766E')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#F8FAFC')),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E2E8F0')),
]))
story.append(t2)
story.append(Paragraph("<b>Table 2:</b> Active mining surface footprint within concentric distance bands of the Son River.", caption_style))

story.append(Spacer(1, 8))
story.append(Paragraph("<b>3.3 Statistical Accuracy Assessment</b>", h2_style))

# Table 3: Confusion Matrix
cm_data = [
    [Paragraph("Predicted \\ Reference", tbl_hdr_style), Paragraph("Mining", tbl_hdr_style), Paragraph("Forest", tbl_hdr_style), Paragraph("Matrix", tbl_hdr_style), Paragraph("Water", tbl_hdr_style), Paragraph("Total", tbl_hdr_style), Paragraph("User's Acc (%)", tbl_hdr_style)],
    [Paragraph("Mining / Pit", tbl_cell_style), "60", "0", "0", "0", "60", "100.00%"],
    [Paragraph("Forest / Canopy", tbl_cell_style), "0", "47", "13", "0", "60", "78.33%"],
    [Paragraph("Matrix / Agri", tbl_cell_style), "1", "11", "48", "0", "60", "80.00%"],
    [Paragraph("Water / River", tbl_cell_style), "2", "0", "1", "57", "60", "95.00%"],
    [Paragraph("<b>Producer's Acc (%)</b>", tbl_cell_style), "<b>95.24%</b>", "<b>81.03%</b>", "<b>77.42%</b>", "<b>100.00%</b>", "240", "<b>OA: 88.33%<br/>κ: 0.8444</b>"]
]
t3 = Table(cm_data, colWidths=[1.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#FFFFFF')),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F1F5F9')),
]))
story.append(t3)
story.append(Paragraph("<b>Table 3:</b> Error contingency matrix and classification accuracy metrics (N = 240 samples).", caption_style))

# Section 4: Discussion & Conclusion
story.append(Spacer(1, 4))
story.append(Paragraph("4. Discussion & Environmental Implications", h1_style))
story.append(Paragraph("The spatial trajectory from 2001 to 2024 demonstrates that mining in the Dhanpuri–Amlai basin transitioned from early, shallow, dispersed scraping toward a highly consolidated, mechanized deep-pit system. The parallel five-fold expansion of vegetative cover reflects both progressive plantation stabilization over backfilled overburden dumps and regional agricultural intensification.", body_style))
story.append(Paragraph("From a riparian protection perspective, the 71.26% reduction of extraction inside the 1 km critical buffer marks substantial spatial retreat away from the Son River trunk channel. However, the persistent presence of 86.51 ha of active mining within this 1 km band represents a key point-source risk for high-suspended-solids runoff during intense monsoon periods, requiring maintained siltation sumps, toe-wall check structures, and permanent vegetative bio-shields along the river's southern bank.", body_style))

story.append(Spacer(1, 4))
story.append(Paragraph("5. Conclusions", h1_style))
story.append(Paragraph("The integration of SWIR brightness thresholds alongside NDVI and MNDWI resolved multi-decadal dry-soil spectral confusion across Landsat sensors, achieving an Overall Accuracy of 88.33% (κ = 0.8444). The study documents positive overburden reclamation trends alongside a critical need for continuous point-source runoff mitigation along the Son River riparian corridor.", body_style))

# Build Document
doc.build(story)
print(f"Publication manuscript generated successfully: {pdf_filename}")