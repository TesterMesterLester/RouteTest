from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Optional
import random

app = FastAPI(title="UK Spirits Sales Dashboard API", version="1.0.0")

# Add CORS middleware for CustomGPT access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# UK Spirits Sales Team Data
SALES_DATA = {
    "sales_reps": [
        {
            "id": 1,
            "name": "James Mitchell",
            "total_sales": 89,
            "sales_this_week": 8,
            "monthly_target": 75,
            "distance_from_target": 14,
            "revenue_generated": 156000,
            "conversion_rate": 28.5,
            "territory": "Thames Valley (Oxford, Reading, Slough)"
        },
        {
            "id": 2,
            "name": "Sarah Williams",
            "total_sales": 94,
            "sales_this_week": 12,
            "monthly_target": 80,
            "distance_from_target": 14,
            "revenue_generated": 172000,
            "conversion_rate": 31.2,
            "territory": "Greater London (Central, North)"
        },
        {
            "id": 3,
            "name": "Michael Thompson",
            "total_sales": 67,
            "sales_this_week": 6,
            "monthly_target": 70,
            "distance_from_target": -3,
            "revenue_generated": 128000,
            "conversion_rate": 24.1,
            "territory": "Home Counties (Surrey, Kent, Essex)"
        },
        {
            "id": 4,
            "name": "Emma Davies",
            "total_sales": 78,
            "sales_this_week": 9,
            "monthly_target": 75,
            "distance_from_target": 3,
            "revenue_generated": 145000,
            "conversion_rate": 26.8,
            "territory": "West London (Ealing, Hounslow, Richmond)"
        }
    ]
}

# Store/Venue Database
VENUES = [
    # Oxford venues
    {
        "uid": "OX001",
        "store_name": "The Eagle & Child",
        "store_address": "49 St Giles', Oxford OX1 3LU",
        "store_owner": "David Henderson",
        "area": "Oxford",
        "venue_type": "Traditional Pub",
        "assigned_rep": 1
    },
    {
        "uid": "OX002", 
        "store_name": "Browns Brasserie Oxford",
        "store_address": "5-11 Woodstock Rd, Oxford OX2 6HA",
        "store_owner": "Maria Santos",
        "area": "Oxford",
        "venue_type": "Restaurant",
        "assigned_rep": 1
    },
    {
        "uid": "OX003",
        "store_name": "The Randolph Hotel Bar",
        "store_address": "Beaumont St, Oxford OX1 2LN", 
        "store_owner": "Robert Clark",
        "area": "Oxford",
        "venue_type": "Hotel Bar",
        "assigned_rep": 1
    },
    {
        "uid": "OX004",
        "store_name": "Turtle Bay Oxford",
        "store_address": "2-5 Bath Pl, Oxford OX1 3SU",
        "store_owner": "Lisa Patel",
        "area": "Oxford",
        "venue_type": "Caribbean Restaurant",
        "assigned_rep": 1
    },
    # Reading venues
    {
        "uid": "RG001",
        "store_name": "London Street Brasserie",
        "store_address": "2-4 London St, Reading RG1 4SE",
        "store_owner": "James Wilson",
        "area": "Reading",
        "venue_type": "Brasserie",
        "assigned_rep": 1
    },
    {
        "uid": "RG002",
        "store_name": "The Purple Turtle",
        "store_address": "1 Gun St, Reading RG1 2JR",
        "store_owner": "Sophie Brown",
        "area": "Reading", 
        "venue_type": "Bar & Club",
        "assigned_rep": 1
    },
    {
        "uid": "RG003",
        "store_name": "Miller & Carter Reading",
        "store_address": "The Forbury, Reading RG1 3EU",
        "store_owner": "Michael Johnson",
        "area": "Reading",
        "venue_type": "Steakhouse",
        "assigned_rep": 1
    },
    {
        "uid": "RG004",
        "store_name": "Slug & Lettuce Reading",
        "store_address": "21-23 King St, Reading RG1 2HE",
        "store_owner": "Amanda Taylor",
        "area": "Reading",
        "venue_type": "Bar & Restaurant",
        "assigned_rep": 1
    }
]

# Sales History (last 90 days)
SALES_HISTORY = [
    {
        "uid": "OX001",
        "date_sold": "2024-06-15",
        "products_sold": [
            {"sku": "MRT-GIN-70", "product_name": "Morningstar Gin 70cl", "quantity": 2, "unit_price": 890},
            {"sku": "BLU-SAP-70", "product_name": "Blue Sapphire Gin 70cl", "quantity": 3, "unit_price": 680}
        ],
        "total_value": 2840,
        "rep_id": 1
    },
    {
        "uid": "OX003", 
        "date_sold": "2024-06-28",
        "products_sold": [
            {"sku": "SLV-DUK-70", "product_name": "Silver Duke Vodka 70cl", "quantity": 2, "unit_price": 1150},
            {"sku": "HIG-12Y-70", "product_name": "Highland Crown 12yr 70cl", "quantity": 1, "unit_price": 1680},
            {"sku": "BLU-SAP-70", "product_name": "Blue Sapphire Gin 70cl", "quantity": 1, "unit_price": 670}
        ],
        "total_value": 4650,
        "rep_id": 1
    },
    {
        "uid": "RG001",
        "date_sold": "2024-07-02",
        "products_sold": [
            {"sku": "ROY-GIN-70", "product_name": "Royal Garden Gin 70cl", "quantity": 3, "unit_price": 720},
            {"sku": "OAK-WHI-70", "product_name": "Oakwood Whiskey 70cl", "quantity": 2, "unit_price": 740}
        ],
        "total_value": 3200,
        "rep_id": 1
    },
    {
        "uid": "RG003",
        "date_sold": "2024-06-20",
        "products_sold": [
            {"sku": "KNG-BLK-70", "product_name": "King's Black Whisky 70cl", "quantity": 2, "unit_price": 890},
            {"sku": "PUR-VOD-70", "product_name": "Purewater Vodka 70cl", "quantity": 3, "unit_price": 400}
        ],
        "total_value": 2980,
        "rep_id": 1
    }
]

# Call Notes with Next Best Actions
CALL_NOTES = [
    {
        "uid": "OX001",
        "last_call_date": "2024-07-10",
        "call_notes": "Spoke to David about new raspberry vodka flavour - DM didn't want to take this on at the time as he had too many other flavoured vodkas",
        "next_best_action": "Review the vodka range to check if the number of flavoured vodkas has reduced such that there might be an opportunity to try to sell in the raspberry vodka again",
        "priority": "Medium"
    },
    {
        "uid": "OX002",
        "last_call_date": "2024-07-08", 
        "call_notes": "Maria interested in premium gin selection for cocktail menu refresh. Mentioned Blue Sapphire performing well but wants something more unique",
        "next_best_action": "Present Morningstar or Royal Garden gin as premium alternatives. Bring cocktail recipe cards to support menu integration",
        "priority": "High"
    },
    {
        "uid": "OX003",
        "last_call_date": "2024-07-05",
        "call_notes": "Robert complained about slow-moving stock on Highland Crown 12yr. Hotel guests preferring more accessible whisky options",
        "next_best_action": "Propose stock rotation deal - swap slow Highland Crown for Oakwood or Riverside whisky. Offer tasting event for hotel guests",
        "priority": "High"
    },
    {
        "uid": "OX004",
        "last_call_date": "2024-07-12",
        "call_notes": "Lisa loves the rum range performance. Golden Spice rum selling exceptionally well. Asked about seasonal rum cocktails",
        "next_best_action": "Introduce Dark Storm spiced rum for Halloween season. Provide tropical rum cocktail recipes for summer menu",
        "priority": "Medium"
    },
    {
        "uid": "RG001",
        "last_call_date": "2024-07-09",
        "call_notes": "James mentioned wine sales dropping, customers shifting to premium spirits. Interested in expanding gin selection",
        "next_best_action": "Propose gin flight tasting boards. Introduce Premium Tonic range to increase per-serve value. Schedule gin masterclass",
        "priority": "High"
    },
    {
        "uid": "RG002",
        "last_call_date": "2024-07-11",
        "call_notes": "Sophie says weekend vodka sales are strong but weekday trade is slow. Looking for promotional ideas",
        "next_best_action": "Suggest 'Vodka Wednesday' promotion. Provide POS materials for Silver Duke and Crystal Clear vodkas. Consider 2-for-1 deals",
        "priority": "Medium"
    },
    {
        "uid": "RG003",
        "last_call_date": "2024-07-06",
        "call_notes": "Michael wants to enhance whisky selection to complement steak menu. Currently only stocks basic options",
        "next_best_action": "Present premium whisky pairing menu. Suggest Highland Crown, Valley Gold, and Smoky Peak whiskies. Offer staff training on whisky & steak pairings",
        "priority": "High"
    },
    {
        "uid": "RG004",
        "last_call_date": "2024-07-13",
        "call_notes": "Amanda reported strong cocktail sales. Bartender skilled and interested in craft cocktails. Wants premium mixer support",
        "next_best_action": "Introduce craft cocktail ingredients and premium spirits. Arrange visit from brand ambassador. Provide cocktail competition entry",
        "priority": "High"
    }
]

@app.get("/")
def root():
    return {
        "message": "UK Spirits Sales Dashboard API", 
        "endpoints": [
            "/leaderboard", 
            "/sales-rep/{rep_id}", 
            "/team-metrics",
            "/venues-in-area",
            "/call-schedule",
            "/sales-history/{uid}"
        ]
    }

@app.get("/leaderboard")
def get_leaderboard():
    """Get UK spirits sales leaderboard"""
    sorted_reps = sorted(SALES_DATA["sales_reps"], key=lambda x: x["total_sales"], reverse=True)
    return {
        "leaderboard": sorted_reps,
        "currency": "GBP",
        "last_updated": datetime.now().isoformat()
    }

@app.get("/sales-rep/{rep_id}")
def get_sales_rep(rep_id: int):
    """Get individual sales rep performance"""
    rep = next((r for r in SALES_DATA["sales_reps"] if r["id"] == rep_id), None)
    if not rep:
        return {"error": "Sales rep not found"}
    
    return {
        "rep_details": rep,
        "ranking": sorted(SALES_DATA["sales_reps"], key=lambda x: x["total_sales"], reverse=True).index(rep) + 1,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/venues-in-area")
def get_venues_in_area(areas: str = Query(..., description="Comma-separated areas (e.g., 'Oxford,Reading')")):
    """Get all venues in specified areas"""
    area_list = [area.strip() for area in areas.split(",")]
    filtered_venues = [venue for venue in VENUES if venue["area"] in area_list]
    
    return {
        "venues": filtered_venues,
        "total_venues": len(filtered_venues),
        "areas_searched": area_list,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/call-schedule")
def get_call_schedule(areas: str = Query(..., description="Comma-separated areas (e.g., 'Oxford,Reading')")):
    """Get comprehensive call schedule with sales history and next actions"""
    area_list = [area.strip() for area in areas.split(",")]
    filtered_venues = [venue for venue in VENUES if venue["area"] in area_list]
    
    # Calculate 90 days ago
    ninety_days_ago = datetime.now() - timedelta(days=90)
    
    call_schedule = []
    for venue in filtered_venues:
        # Check if sold to in last 90 days
        recent_sale = next((sale for sale in SALES_HISTORY 
                          if sale["uid"] == venue["uid"] and 
                          datetime.fromisoformat(sale["date_sold"]) >= ninety_days_ago), None)
        
        # Get call notes
        call_note = next((note for note in CALL_NOTES if note["uid"] == venue["uid"]), None)
        
        venue_data = {
            **venue,
            "sold_last_90_days": recent_sale is not None,
            "last_sale_date": recent_sale["date_sold"] if recent_sale else None,
            "last_sale_value": recent_sale["total_value"] if recent_sale else None,
            "last_sale_products": recent_sale["products_sold"] if recent_sale else [],
            "last_sale_skus": [f"{item['sku']} - {item['product_name']} (Qty: {item['quantity']})" 
                              for item in recent_sale["products_sold"]] if recent_sale else [],
            "call_notes": call_note["call_notes"] if call_note else "No recent call notes",
            "next_best_action": call_note["next_best_action"] if call_note else "Schedule introductory call",
            "priority": call_note["priority"] if call_note else "Low",
            "last_call_date": call_note["last_call_date"] if call_note else "No recent calls"
        }
        call_schedule.append(venue_data)
    
    return {
        "call_schedule": call_schedule,
        "total_venues": len(call_schedule),
        "areas_searched": area_list,
        "venues_with_recent_sales": len([v for v in call_schedule if v["sold_last_90_days"]]),
        "high_priority_actions": len([v for v in call_schedule if v["priority"] == "High"]),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/sales-history/{uid}")
def get_sales_history(uid: str):
    """Get sales history for a specific venue"""
    venue = next((v for v in VENUES if v["uid"] == uid), None)
    if not venue:
        return {"error": "Venue not found"}
    
    sales = [sale for sale in SALES_HISTORY if sale["uid"] == uid]
    
    return {
        "venue_details": venue,
        "sales_history": sales,
        "total_sales": len(sales),
        "total_value": sum(sale["total_value"] for sale in sales),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/team-metrics")
def get_team_metrics():
    """Get overall team performance metrics"""
    total_sales = sum(rep["total_sales"] for rep in SALES_DATA["sales_reps"])
    total_revenue = sum(rep["revenue_generated"] for rep in SALES_DATA["sales_reps"])
    
    return {
        "team_performance": {
            "total_team_sales": total_sales,
            "total_team_revenue": total_revenue,
            "currency": "GBP",
            "average_conversion_rate": sum(rep["conversion_rate"] for rep in SALES_DATA["sales_reps"]) / len(SALES_DATA["sales_reps"])
        },
        "top_performer": max(SALES_DATA["sales_reps"], key=lambda x: x["total_sales"]),
        "needs_attention": [rep for rep in SALES_DATA["sales_reps"] if rep["distance_from_target"] < 0],
        "last_updated": datetime.now().isoformat()
    }
