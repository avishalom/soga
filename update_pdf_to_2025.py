#!/usr/bin/env python3
"""
Script to update SOGA Waiver Form from 2023 to 2025
Uses reportlab to recreate the PDF with updated dates
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def create_soga_waiver_2025():
    """Create the SOGA Waiver Form PDF for 2025"""
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        "/Users/vishshalit/gith/soga/SOGA-Waiver-Form-2025.pdf",
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=8,
        leftIndent=0,
        rightIndent=0
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=4,
        leftIndent=20,
        rightIndent=0
    )
    
    # Content for the PDF
    story = []
    
    # Page 1
    story.append(Paragraph("SOGA Waiver Form - 2025", title_style))
    story.append(Paragraph("INFORMED CONSENT, ASSUMPTION OF RISK, and<br/>WAIVER OF LIABILITY", subtitle_style))
    
    # Main content paragraphs with bullet points (represented by •)
    paragraphs = [
        "• <b>THIS IS A LEGAL CONTRACT</b> between me, _________________________ and Southwestern Ontario Gliding Association (\"SOGA\"), a hang gliding club which includes both individually and collectively all pilots, instructors, employees, agents, ground crew, tug pilots, volunteers, equipment owners and operators. This contract also indemnifies Her Majesty the Queen in Right of Canada, Rick Dewsbury and Jocelyne Dewsbury, and any other landowners or leaseholders.",
        
        "• <b>SIGNING THIS IS PART OF THE PRICE I AM PAYING</b> for being allowed to engage in hang gliding activities which includes, but is not limited to, launching, flying, or landing a hang glider, as a pilot, passenger, assistant, or spectator, riding or driving the golf cart, flying a tow aircraft, operating a winch, or any other activity incidental to instruction, participation in the sport of hang gliding (which includes Paragliding) or enabling, assisting or facilitating the participation of others in the same. I will conduct myself in all respects and at all times in a responsible and safe manner so as to minimize the danger to my life and property, and that of others.",
        
        "• <b>THERE IS NO INSURANCE and NO WARRANTY</b> of fitness for any purpose on any of the equipment used in the instruction or flights. I accept the equipment used in my hang gliding activities \"as is\". I acknowledge that my hang gliding activities are not covered by any personal accident or general liability insurance covering SOGA.",
        
        "• <b>I KNOW AND ACCEPT THAT HANG GLIDING IS DANGEROUS.</b> I voluntarily accept all risks of participation in hang gliding activities, the dangers I know about, and those that I don't; the dangers that are foreseeable and those that are not; even if caused in whole or in part by the action, inaction, or negligence of SOGA. I accept that no amount of care, caution, instruction, or expertise can eliminate all of the risks. I accept that as a result of the risks, I may be injured, my property may be damaged or destroyed, and I may even die.",
        
        "• <b>I EXEMPT, RELEASE, and INDEMNIFY SOGA</b> from any and all liability, claims, demands, or causes of action arising from any property damage, bodily injury, or death as a result of hang gliding activities. No damages, compensation, or other award will be payable to me or my estate by SOGA either individually or collectively in respect of any loss, damage, injury, or death. I will not sue or start any type of action that directly or indirectly requires compensation or defence by SOGA. This is binding on my estate, heirs, survivors, assigns, executors, administrators, and legal representatives.",
        
        "• <b>I ASSUME FULL AND SOLE FINANCIAL RESPONSIBILITY</b> for any damages I may suffer or cause while participating in hang gliding activities. I waive and repudiate the protection of any law or legal principle that would limit the effect of this contract."
    ]
    
    for para in paragraphs:
        story.append(Paragraph(para, body_style))
        story.append(Spacer(1, 6))
    
    # Page footer
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Page 1 of 2</b>", ParagraphStyle('PageNum', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)))
    
    # Page break
    story.append(PageBreak())
    
    # Page 2
    story.append(Paragraph("SOGA Waiver Form - 2025", title_style))
    story.append(Paragraph("INFORMED CONSENT, ASSUMPTION OF RISK, and<br/>WAIVER OF LIABILITY", subtitle_style))
    
    # Page 2 content
    page2_paragraphs = [
        "• <b>I INDEMNIFY AND HOLD HARMLESS \"SOGA\"</b> from any damages or losses caused to any other person resulting from my hang gliding activities.",
        
        "• <b>I AGREE</b> that this consent, assumption of risk, indemnity, and waiver of liability remains in full force and effect so long as I continue to engage in hang gliding activities with SOGA or any related entity. This contract remains in full legal force indefinitely unless revoked in writing."
    ]
    
    for para in page2_paragraphs:
        story.append(Paragraph(para, body_style))
        story.append(Spacer(1, 6))
    
    # Legal evidence section
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>THIS DOCUMENT IS EVIDENCE IN A COURT OF LAW</b>", body_style))
    
    legal_items = [
        "a) My signature on this document constitutes an irrevocable admission of the facts stated herein.",
        "b) This document is my own statement in every respect.",
        "c) I have made no statements to SOGA that conflict with, limit, or modify this contract, and SOGA has said nothing conflicting with this statement to me.",
        "d) I have had the unhurried opportunity to ask questions of SOGA, and have been given answers satisfactory to me.",
        "e) I have had sufficient time to reflect and consider the full implications of entering into this contract.",
        "f) I acknowledge that I either have had independent legal advice, or I have decided, after reflection, that I don't want independent legal advice before signing.",
        "g) Any legal issue arising from this contract shall be dealt with in the Ontario Superior Court of Justice in Kitchener/Waterloo. I attorn to the jurisdiction of that court."
    ]
    
    for item in legal_items:
        story.append(Paragraph(item, bullet_style))
    
    # Signature section
    story.append(Spacer(1, 24))
    story.append(Paragraph("SIGNED at _______________, Ontario on the _____ day of __________________, <b>2025</b>", body_style))
    story.append(Spacer(1, 24))
    
    # Signature lines
    story.append(Paragraph("_____________________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;___________________________", body_style))
    story.append(Paragraph("(signature of participant)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(signature of witness for SOGA)", body_style))
    story.append(Spacer(1, 12))
    
    # Contact information
    story.append(Paragraph("Name: ________________________________________ (please print)", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Address: _________________________________________________________________________", body_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(street)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(city)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(province)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(postal code)", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Phone: _(______)____________________&nbsp;&nbsp;&nbsp;&nbsp;email address ________________________________", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Emergency Contact Name: _____________________________&nbsp;&nbsp;&nbsp;&nbsp;Phone: _(____)_____________", body_style))
    story.append(Spacer(1, 12))
    
    # Note
    story.append(Paragraph("<b>Note:</b> Please put your initials in each oval to signify that you have read, and fully understand, each of the adjacent paragraphs.", body_style))
    story.append(Spacer(1, 12))
    
    # Page footer
    story.append(Paragraph("<b>Page 2 of 2</b>", ParagraphStyle('PageNum', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)))
    story.append(Spacer(1, 8))
    story.append(Paragraph("April 15, 2025", ParagraphStyle('Date', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER)))
    
    # Build the PDF
    doc.build(story)
    print("✅ Successfully created SOGA-Waiver-Form-2025.pdf with updated 2025 dates!")

if __name__ == "__main__":
    try:
        create_soga_waiver_2025()
    except ImportError as e:
        print(f"❌ Missing required library: {e}")
        print("💡 Install with: pip install reportlab")
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")