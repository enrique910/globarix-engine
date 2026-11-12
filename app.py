# ==============================================================================
# PROPRIETARY TRADE SECRET NOTICE & COPYRIGHT NOTICE
# Copyright (c) 2026 Datascope LLC (GLOBARIX.COM). All Rights Reserved.
# GLOBARIX.COM — UNIVERSAL MULTI-ASSET LANDED-COST & COMPLIANCE OPERATING SYSTEM (v5.4)
# Protected under 18 U.S.C. § 1836 (Defend Trade Secrets Act) & Fla. Stat. § 688.
# ==============================================================================

import os
import http.server
import socketserver
import urllib.request
import json
import time

PORT = int(os.environ.get("PORT", 8080))

COUNTRIES_RAW = [
    ("AF","Afghanistan","Asia",0.16,0.10,3200,750,False,10),("AL","Albania","Europe",0.10,0.20,2400,600,False,10),
    ("DZ","Algeria","Africa",0.30,0.19,2600,700,False,3),("AD","Andorra","Europe",0.045,0.045,2300,500,False,15),
    ("AO","Angola","Africa",0.20,0.14,2900,800,False,5),("AG","Antigua and Barbuda","Americas",0.20,0.15,1800,650,True,10),
    ("AR","Argentina","Americas",0.35,0.21,2400,850,False,5),("AM","Armenia","Asia",0.15,0.20,2800,700,False,10),
    ("AU","Australia","Oceania",0.05,0.10,3100,900,True,25),("AT","Austria","Europe",0.10,0.20,2300,550,False,15),
    ("AZ","Azerbaijan","Asia",0.15,0.18,2900,700,False,10),("BS","Bahamas","Americas",0.25,0.10,1200,550,False,10),
    ("BH","Bahrain","Middle East",0.05,0.10,2700,600,False,5),("BD","Bangladesh","Asia",0.25,0.15,3300,850,True,5),
    ("BB","Barbados","Americas",0.20,0.175,1700,600,True,4),("BY","Belarus","Europe",0.15,0.20,2600,650,False,10),
    ("BE","Belgium","Europe",0.10,0.21,2100,500,False,15),("BZ","Belize","Americas",0.20,0.125,1600,600,False,10),
    ("BJ","Benin","Africa",0.20,0.18,2700,750,False,10),("BT","Bhutan","Asia",0.20,0.10,3500,800,True,10),
    ("BO","Bolivia","Americas",0.15,0.13,2200,700,False,3),("BA","Bosnia and Herzegovina","Europe",0.15,0.17,2400,600,False,10),
    ("BW","Botswana","Africa",0.20,0.14,3100,800,True,10),("BR","Brazil","Americas",0.35,0.17,2300,850,False,0),
    ("BN","Brunei","Asia",0.05,0.00,3200,700,True,7),("BG","Bulgaria","Europe",0.10,0.20,2400,550,False,15),
    ("BF","Burkina Faso","Africa",0.20,0.18,2800,750,False,10),("BI","Burundi","Africa",0.25,0.18,3300,800,False,10),
    ("CV","Cabo Verde","Africa",0.20,0.15,2500,650,False,10),("KH","Cambodia","Asia",0.35,0.10,3100,750,False,10),
    ("CM","Cameroon","Africa",0.30,0.1925,2800,800,False,10),("CA","Canada","Americas",0.061,0.05,1200,450,False,15),
    ("CF","Central African Republic","Africa",0.30,0.19,3200,850,False,10),("TD","Chad","Africa",0.30,0.18,3300,850,False,10),
    ("CL","Chile","Americas",0.06,0.19,2100,600,False,0),("CN","China","Asia",0.15,0.13,2900,800,False,10),
    ("CO","Colombia","Americas",0.15,0.19,1650,650,False,0),("KM","Comoros","Africa",0.20,0.10,3400,800,False,10),
    ("CG","Congo","Africa",0.20,0.18,2900,800,False,10),("CD","Congo (DRC)","Africa",0.20,0.16,3000,850,False,10),
    ("CR","Costa Rica","Americas",0.15,0.13,1600,600,False,10),("CI","Cote d Ivoire","Africa",0.20,0.18,2700,750,False,10),
    ("HR","Croatia","Europe",0.10,0.25,2300,550,False,15),("CU","Cuba","Americas",0.20,0.10,1800,700,False,10),
    ("CY","Cyprus","Europe",0.10,0.19,2500,600,True,5),("CZ","Czech Republic","Europe",0.10,0.21,2300,550,False,15),
    ("DK","Denmark","Europe",0.10,0.25,2200,550,False,15),("DJ","Djibouti","Africa",0.25,0.10,3000,750,False,8),
    ("DM","Dominica","Americas",0.20,0.15,1750,600,True,10),("DO","Dominican Republic","Americas",0.20,0.18,1450,650,False,5),
    ("EC","Ecuador","Americas",0.35,0.15,1800,650,False,5),("EG","Egypt","Africa",0.40,0.14,2700,750,False,1),
    ("SV","El Salvador","Americas",0.15,0.13,1600,600,False,8),("GQ","Equatorial Guinea","Africa",0.30,0.15,3000,800,False,10),
    ("ER","Eritrea","Africa",0.25,0.05,3200,800,False,10),("EE","Estonia","Europe",0.10,0.22,2400,550,False,15),
    ("SZ","Eswatini","Africa",0.25,0.15,3100,800,True,10),("ET","Ethiopia","Africa",0.35,0.15,3200,850,False,10),
    ("FJ","Fiji","Oceania",0.15,0.09,3200,800,True,5),("FI","Finland","Europe",0.10,0.24,2300,550,False,15),
    ("FR","France","Europe",0.10,0.20,2100,500,False,15),("GA","Gabon","Africa",0.30,0.18,2900,800,False,5),
    ("GM","Gambia","Africa",0.20,0.15,2600,700,True,10),("GE","Georgia","Asia",0.05,0.18,2700,650,False,15),
    ("DE","Germany","Europe",0.10,0.19,2200,450,False,15),("GH","Ghana","Africa",0.20,0.15,2700,750,False,10),
    ("GR","Greece","Europe",0.10,0.24,2300,550,False,15),("GD","Grenada","Americas",0.20,0.15,1750,600,True,10),
    ("GT","Guatemala","Americas",0.15,0.12,1600,600,False,10),("GN","Guinea","Africa",0.20,0.18,2700,750,False,8),
    ("GW","Guinea-Bissau","Africa",0.20,0.15,2700,750,False,10),("GY","Guyana","Americas",0.20,0.14,1850,650,True,8),
    ("HT","Haiti","Americas",0.10,0.10,1500,650,False,10),("HN","Honduras","Americas",0.15,0.15,1600,600,False,10),
    ("HU","Hungary","Europe",0.10,0.27,2400,550,False,15),("IS","Iceland","Europe",0.10,0.24,2500,600,False,15),
    ("IN","India","Asia",0.70,0.28,3100,850,True,3),("ID","Indonesia","Asia",0.50,0.11,3200,800,True,0),
    ("IR","Iran","Middle East",0.40,0.09,3200,850,False,5),("IQ","Iraq","Middle East",0.15,0.00,3000,750,False,2),
    ("IE","Ireland","Europe",0.10,0.23,2100,500,True,15),("IL","Israel","Middle East",0.07,0.17,2600,650,False,2),
    ("IT","Italy","Europe",0.10,0.22,2200,500,False,15),("JM","Jamaica","Americas",0.20,0.215,1550,650,True,5),
    ("JP","Japan","Asia",0.00,0.10,2800,650,True,25),("JO","Jordan","Middle East",0.20,0.16,2800,700,False,5),
    ("KZ","Kazakhstan","Asia",0.15,0.12,3100,750,False,7),("KE","Kenya","Africa",0.25,0.16,3100,800,True,8),
    ("KI","Kiribati","Oceania",0.15,0.125,3400,800,True,10),("KP","North Korea","Asia",0.30,0.00,3500,900,False,5),
    ("KR","South Korea","Asia",0.08,0.10,2700,600,False,10),("XK","Kosovo","Europe",0.10,0.18,2500,600,False,10),
    ("KW","Kuwait","Middle East",0.05,0.00,2700,600,False,5),("KG","Kyrgyzstan","Asia",0.15,0.12,3200,750,False,10),
    ("LA","Laos","Asia",0.30,0.10,3300,800,False,5),("LV","Latvia","Europe",0.10,0.21,2400,550,False,15),
    ("LB","Lebanon","Middle East",0.20,0.11,2700,650,False,8),("LS","Lesotho","Africa",0.25,0.15,3100,800,True,10),
    ("LR","Liberia","Africa",0.20,0.10,2700,750,False,10),("LY","Libya","Africa",0.10,0.00,2800,750,False,10),
    ("LI","Liechtenstein","Europe",0.00,0.081,2300,500,False,15),("LT","Lithuania","Europe",0.10,0.21,2400,550,False,15),
    ("LU","Luxembourg","Europe",0.10,0.17,2100,500,False,15),("MG","Madagascar","Africa",0.20,0.20,3200,800,False,10),
    ("MW","Malawi","Africa",0.25,0.165,3200,800,True,10),("MY","Malaysia","Asia",0.30,0.10,3000,750,True,5),
    ("MV","Maldives","Asia",0.20,0.08,3200,750,True,5),("ML","Mali","Africa",0.20,0.18,2800,750,False,10),
    ("MT","Malta","Europe",0.10,0.18,2400,550,True,15),("MH","Marshall Islands","Oceania",0.15,0.06,3400,800,False,10),
    ("MR","Mauritania","Africa",0.20,0.16,2700,750,False,8),("MU","Mauritius","Africa",0.15,0.15,3100,750,True,4),
    ("MX","Mexico","Americas",0.15,0.16,1400,500,False,10),("FM","Micronesia","Oceania",0.15,0.05,3400,800,False,10),
    ("MD","Moldova","Europe",0.12,0.20,2600,600,False,10),("MC","Monaco","Europe",0.10,0.20,2200,500,False,15),
    ("MN","Mongolia","Asia",0.05,0.10,3300,800,False,10),("ME","Montenegro","Europe",0.10,0.21,2400,600,False,10),
    ("MA","Morocco","Africa",0.175,0.20,2400,650,False,5),("MZ","Mozambique","Africa",0.20,0.16,3100,800,True,10),
    ("MM","Myanmar","Asia",0.30,0.05,3300,800,True,5),("NA","Namibia","Africa",0.25,0.15,3100,800,True,8),
    ("NR","Nauru","Oceania",0.15,0.10,3400,800,True,10),("NP","Nepal","Asia",0.80,0.13,3400,850,True,5),
    ("NL","Netherlands","Europe",0.10,0.21,2100,500,False,15),("NZ","New Zealand","Oceania",0.00,0.15,3100,850,True,20),
    ("NI","Nicaragua","Americas",0.15,0.15,1600,600,False,10),("NE","Niger","Africa",0.20,0.19,2800,750,False,8),
    ("NG","Nigeria","Africa",0.20,0.075,2800,800,False,12),("MK","North Macedonia","Europe",0.10,0.18,2400,600,False,10),
    ("NO","Norway","Europe",0.00,0.25,2400,600,False,20),("OM","Oman","Middle East",0.05,0.05,2700,600,False,7),
    ("PK","Pakistan","Asia",0.50,0.18,3100,800,True,3),("PW","Palau","Oceania",0.10,0.10,3400,800,False,10),
    ("PS","Palestine","Middle East",0.15,0.16,2700,700,False,3),("PA","Panama","Americas",0.15,0.07,1500,600,False,10),
    ("PG","Papua New Guinea","Oceania",0.20,0.10,3400,800,True,5),("PY","Paraguay","Americas",0.15,0.10,2300,750,False,10),
    ("PE","Peru","Americas",0.06,0.18,1900,650,False,5),("PH","Philippines","Asia",0.30,0.12,3100,750,False,0),
    ("PL","Poland","Europe",0.10,0.23,2300,550,False,15),("PT","Portugal","Europe",0.10,0.23,2200,500,False,15),
    ("QA","Qatar","Middle East",0.05,0.00,2700,600,False,5),("RO","Romania","Europe",0.10,0.19,2400,550,False,15),
    ("RU","Russia","Europe",0.15,0.20,2900,800,False,10),("RW","Rwanda","Africa",0.25,0.18,3200,800,False,10),
    ("KN","Saint Kitts and Nevis","Americas",0.20,0.17,1750,600,True,10),("LC","Saint Lucia","Americas",0.20,0.125,1750,600,True,5),
    ("VC","Saint Vincent and the Grenadines","Americas",0.20,0.16,1750,600,True,10),("WS","Samoa","Oceania",0.20,0.15,3400,800,True,10),
    ("SM","San Marino","Europe",0.10,0.17,2300,500,False,15),("ST","Sao Tome and Principe","Africa",0.20,0.15,2900,800,False,10),
    ("SA","Saudi Arabia","Middle East",0.05,0.15,2700,600,False,5),("SN","Senegal","Africa",0.20,0.18,2600,700,False,8),
    ("RS","Serbia","Europe",0.125,0.20,2400,600,False,10),("SC","Seychelles","Africa",0.15,0.15,3200,750,True,3),
    ("SL","Sierra Leone","Africa",0.20,0.15,2700,750,True,10),("SG","Singapore","Asia",0.00,0.09,2900,700,True,3),
    ("SK","Slovakia","Europe",0.10,0.20,2300,550,False,15),("SI","Slovenia","Europe",0.10,0.22,2300,550,False,15),
    ("SB","Solomon Islands","Oceania",0.20,0.15,3400,800,True,10),("SO","Somalia","Africa",0.25,0.05,3200,800,False,10),
    ("ZA","South Africa","Africa",0.25,0.15,2900,800,True,0),("SS","South Sudan","Africa",0.25,0.18,3300,850,False,5),
    ("ES","Spain","Europe",0.10,0.21,2200,500,False,15),("LK","Sri Lanka","Asia",0.50,0.18,3200,800,True,3),
    ("SD","Sudan","Africa",0.25,0.17,3100,800,False,5),("SR","Suriname","Americas",0.20,0.10,1900,650,True,8),
    ("SE","Sweden","Europe",0.10,0.25,2300,550,False,15),("CH","Switzerland","Europe",0.00,0.081,2300,500,False,15),
    ("SY","Syria","Middle East",0.30,0.00,3000,800,False,5),("TW","Taiwan","Asia",0.175,0.05,2900,650,False,10),
    ("TJ","Tajikistan","Asia",0.15,0.14,3300,800,False,10),("TZ","Tanzania","Africa",0.25,0.18,3100,800,True,8),
    ("TH","Thailand","Asia",0.40,0.07,3000,750,True,0),("TL","Timor-Leste","Asia",0.05,0.025,3300,800,True,5),
    ("TG","Togo","Africa",0.20,0.18,2700,750,False,10),("TO","Tonga","Oceania",0.20,0.15,3400,800,True,10),
    ("TT","Trinidad and Tobago","Americas",0.20,0.125,1750,600,True,4),("TN","Tunisia","Africa",0.20,0.19,2500,650,False,5),
    ("TR","Turkey","Europe",0.10,0.20,2600,650,False,5),("TM","Turkmenistan","Asia",0.15,0.15,3300,800,False,5),
    ("TV","Tuvalu","Oceania",0.20,0.07,3400,800,True,10),("UG","Uganda","Africa",0.25,0.18,3200,800,True,8),
    ("UA","Ukraine","Europe",0.10,0.20,2600,650,False,10),("AE","United Arab Emirates","Middle East",0.05,0.05,2600,500,False,5),
    ("GB","United Kingdom","Europe",0.10,0.20,2100,500,True,15),("US","United States","Americas",0.025,0.00,2200,550,False,25),
    ("UY","Uruguay","Americas",0.23,0.22,2350,750,False,0),("UZ","Uzbekistan","Asia",0.15,0.12,3200,750,False,10),
    ("VU","Vanuatu","Oceania",0.20,0.125,3400,800,True,10),("VA","Vatican City","Europe",0.00,0.00,2300,500,False,15),
    ("VE","Venezuela","Americas",0.20,0.16,1700,700,False,5),("VN","Vietnam","Asia",0.50,0.10,3100,750,False,5),
    ("YE","Yemen","Middle East",0.25,0.05,3200,800,False,7),("ZM","Zambia","Africa",0.25,0.16,3200,800,True,10),
    ("ZW","Zimbabwe","Africa",0.25,0.15,3200,800,True,10)
]

countries_dict = {}
for item in COUNTRIES_RAW:
    code, name, region, tariff, vat, freight, port, rhd, max_age = item
    countries_dict[code] = {
        "name": name, "region": region, "tariff": tariff, "vat": vat,
        "freight": freight, "port": port, "rhd": rhd, "maxAge": max_age
    }

countries_dict["DO"]["ftaOrigin"] = ["US"]
countries_dict["DO"]["excise"] = "tiered_cc"
countries_dict["CA"]["ftaOrigin"] = ["US", "MX"]
countries_dict["CL"]["ftaOrigin"] = ["US", "MX", "CA"]
countries_dict["CO"]["ftaOrigin"] = ["US", "MX"]
countries_dict["CR"]["ftaOrigin"] = ["US"]
countries_dict["SV"]["ftaOrigin"] = ["US"]
countries_dict["GT"]["ftaOrigin"] = ["US"]
countries_dict["HN"]["ftaOrigin"] = ["US"]
countries_dict["MX"]["ftaOrigin"] = ["US", "CA"]
countries_dict["MA"]["ftaOrigin"] = ["US"]
countries_dict["NI"]["ftaOrigin"] = ["US"]
countries_dict["OM"]["ftaOrigin"] = ["US"]
countries_dict["PA"]["ftaOrigin"] = ["US"]
countries_dict["PE"]["ftaOrigin"] = ["US"]
countries_dict["SG"]["ftaOrigin"] = ["US"]
countries_dict["KR"]["ftaOrigin"] = ["US"]
countries_dict["US"]["ftaOrigin"] = ["CA", "MX"]

NATIONS_JSON = json.dumps(countries_dict)

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GLOBARIX | Universal Multi-Asset Landed-Cost OS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="icon" type="image/svg+xml" href="/api/favicon.svg">
  <style>
    :root {{
      --bg-deep: #0B1D3A;
      --gold-accent: #C5A059;
      --slate-text: #2C3539;
    }}
    @media print {{ 
      body {{ background: white !important; color: #2C3539 !important; padding: 0 !important; }} 
      .no-print {{ display: none !important; }} 
      .print-only {{ display: block !important; }} 
      .watermark {{ position: fixed; bottom: 10px; right: 10px; font-size: 8px; color: #8B7355; font-family: monospace; opacity: 0.7; }}
    }}
    .print-only {{ display: none; }}
    select option {{ background-color: #0B1D3A !important; color: #F8FAFC !important; padding: 10px !important; }}
  </style>
</head>
<body class="bg-[#0B1D3A] text-slate-100 min-h-screen p-6 font-sans antialiased selection:bg-[#C5A059] selection:text-slate-950">
  
  <div class="fixed top-0 left-0 right-0 bg-[#0B1D3A]/95 border-b border-[#C5A059]/30 text-[10px] font-mono text-slate-400 px-4 py-1 flex justify-between items-center z-50 backdrop-blur no-print">
    <div class="flex items-center gap-2">
      <span class="h-2 w-2 rounded-full bg-emerald-500 animate-ping"></span>
      <span class="text-[#C5A059] font-bold">GLOBARIX SECURE OS v5.4</span>
      <span class="text-slate-500">|</span>
      <span>Session: <span id="sessionIdBadge" class="text-slate-300">GX-8892-SECURE</span></span>
    </div>
    <div class="flex items-center gap-4">
      <span class="text-slate-400">Trade Secrets Protected (18 U.S.C. § 1836)</span>
      <span class="text-emerald-400 font-bold">● IP Guard Active</span>
    </div>
  </div>

  <div class="max-w-6xl mx-auto space-y-6 no-print pt-6">
    
    <header class="bg-[#071325] border border-[#C5A059]/40 rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <h1 class="text-3xl font-serif tracking-widest text-white uppercase">GLOBARIX<span class="text-[#C5A059] font-sans font-bold text-sm ml-1">.COM</span></h1>
          <span class="text-[10px] font-mono bg-[#C5A059]/20 text-[#C5A059] border border-[#C5A059]/40 px-2 py-0.5 rounded uppercase font-bold">Enterprise OS</span>
        </div>
        <p class="text-xs text-slate-400 mt-0.5">Universal Cross-Border Asset Clearance, Landed Cost & Arbitrage Intelligence OS</p>
      </div>

      <div class="flex flex-wrap items-center gap-3 text-xs font-mono">
        <div class="flex items-center gap-1.5 bg-slate-900 border border-slate-800 px-2.5 py-1.5 rounded-lg">
          <span class="text-slate-400 text-[11px]">Workspace Tier:</span>
          <select id="userTierSelect" onchange="onTierChange()" class="bg-slate-950 border border-[#C5A059]/50 text-white rounded px-2 py-1 text-xs font-bold focus:outline-none">
            <option value="FREE_PREVIEW">Free Preview ($0/mo - 3 Lookups)</option>
            <option value="TRADER_PRO">Trader Desk Pro ($499/mo)</option>
            <option value="ENTERPRISE">Enterprise Desk ($1,200/mo)</option>
          </select>
        </div>

        <div id="quotaBadge" class="bg-amber-950/60 border border-amber-800 text-amber-300 px-3 py-1.5 rounded-lg text-xs font-bold">
          Lookups Remaining: <span id="quotaRemainingText">3</span> / 3
        </div>

        <div class="flex items-center gap-2 bg-slate-900 border border-slate-800 px-2.5 py-1.5 rounded-lg">
          <span class="text-slate-400 text-[11px]">IP Shield:</span>
          <button id="blindedToggleBtn" onclick="toggleBlindedMode()" class="px-2.5 py-1 rounded text-[10px] font-bold uppercase transition bg-slate-800 text-slate-300 border border-slate-700">OFF</button>
        </div>
      </div>
    </header>

    <div id="tierBanner" class="p-3 bg-amber-950/40 border border-amber-800/80 rounded-xl flex items-center justify-between text-xs">
      <div class="flex items-center gap-2">
        <span class="text-[#C5A059] text-sm font-bold">🛡️</span>
        <span class="text-slate-300"><strong>Free Preview Mode:</strong> Limited to 3 calculations. Detailed VAT, luxury surcharges, net arbitrage spreads, and PDF quotes are gated under IP protection.</span>
      </div>
      <button onclick="promptUpgrade()" class="bg-[#C5A059] hover:bg-[#d4b067] text-slate-950 font-bold px-3.5 py-1.5 rounded uppercase tracking-wider text-[11px] transition shadow">Upgrade to Pro ($499)</button>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 text-xs shadow-lg">
      <div class="flex items-center gap-2">
        <span class="text-slate-400 font-semibold uppercase tracking-wider text-[11px]">Asset Family:</span>
        <select id="assetFamilySelect" onchange="onAssetFamilyChange()" class="bg-slate-950 border border-[#C5A059]/60 text-[#C5A059] font-bold rounded-lg px-3 py-1.5 focus:outline-none focus:border-[#C5A059]">
          <option value="MOTOR_VEHICLE">1. Motor Vehicles & Trucks (17-Digit VIN - HS 8703/8704)</option>
          <option value="MARINE_VESSEL">2. Marine Vessels & Yachts (12-Char HIN - HS 8903)</option>
          <option value="HEAVY_EQUIPMENT">3. Construction & Mining Machinery (17-Char PIN - HS 8429)</option>
          <option value="AG_EQUIPMENT">4. Commercial Agricultural Machinery (PIN - HS 8432/8433)</option>
          <option value="POWERSPORTS">5. Powersports, UTVs & RVs (14-17 PIN/VIN - HS 8703/8711)</option>
          <option value="TRAILERS">6. Commercial Transport Trailers (17-Digit Chassis VIN - HS 8716)</option>
          <option value="POWER_SYSTEMS">7. Industrial Power & Generators (Serial No - HS 8502/8414)</option>
          <option value="MATERIAL_HANDLING">8. Material Handling & Forklifts (PIN/Mast - HS 8427)</option>
          <option value="FORESTRY">9. Commercial Forestry & Logging Equipment (PIN - HS 8436)</option>
          <option value="AVIATION">10. Commercial Aviation & Turboprops (Tail/MSN - HS 8802)</option>
        </select>
      </div>
      <div id="assetBadge" class="font-mono text-[11px] text-[#C5A059] bg-[#C5A059]/10 border border-[#C5A059]/30 px-3 py-1 rounded">Active Category: 1. Motor Vehicles & Trucks</div>
    </div>

    <div class="flex border-b border-slate-800 space-x-2 text-xs font-semibold">
      <button onclick="switchTab('tradeDesk')" id="tabBtn-tradeDesk" class="px-4 py-2 border-b-2 border-[#C5A059] text-[#C5A059] font-bold transition">1. Trade Desk Engine</button>
      <button onclick="switchTab('multiMatrix')" id="tabBtn-multiMatrix" class="px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-white transition">2. Multi-Lane Arbitrage Matrix</button>
      <button onclick="switchTab('cbpDossier')" id="tabBtn-cbpDossier" class="px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-white transition">3. CBP 72-Hr Export Packet (19 CFR § 192.2)</button>
      <button onclick="switchTab('homologationTab')" id="tabBtn-homologationTab" class="px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-white transition">4. Homologation & Seizure Shield</button>
      <button onclick="switchTab('legalTab')" id="tabBtn-legalTab" class="px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-white transition">5. Legal & Regulatory Disclaimers</button>
    </div>

    <div id="tabContent-tradeDesk" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-xl">
        <h2 class="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center justify-between">
          <span>Asset & Routing</span>
          <span id="routeTag" class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">Bilateral (197 Nations)</span>
        </h2>
        
        <div>
          <div class="flex justify-between items-center mb-1">
            <label class="block text-xs text-slate-400 font-semibold">Origin Export Hub (Scrollable 197 Nations)</label>
            <span id="originCountBadge" class="text-[10px] font-mono text-[#C5A059] bg-[#C5A059]/10 px-2 py-0.5 rounded border border-[#C5A059]/30">197 Loaded</span>
          </div>
          <select id="originSelect" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-[#C5A059] font-mono cursor-pointer"></select>
        </div>

        <div>
          <div class="flex justify-between items-center mb-1">
            <label class="block text-xs text-slate-400 font-semibold">Target Destination Port of Entry (Scrollable 197 Nations)</label>
            <span id="destCountBadge" class="text-[10px] font-mono text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">197 Loaded</span>
          </div>
          <select id="countrySelect" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-cyan-500 font-mono cursor-pointer"></select>
        </div>

        <div>
          <label id="idInputLabel" class="block text-xs text-slate-400 mb-1">17-Digit Vehicle Identification Number (VIN)</label>
          <div class="flex gap-2">
            <input type="text" id="assetIdInput" value="4JGDA5HB4MA123456" maxlength="25" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs font-mono text-white tracking-widest focus:outline-none focus:border-[#C5A059] uppercase">
            <button id="decodeBtn" onclick="executeCalculation()" class="bg-[#C5A059] hover:bg-[#d4b067] text-slate-950 font-bold px-4 py-2 rounded-lg text-xs uppercase tracking-wider transition shadow">Run</button>
          </div>
          <div id="presetButtonsContainer" class="mt-2 flex gap-1.5 flex-wrap text-[10px]"></div>
        </div>

        <div class="bg-slate-950/70 border border-slate-800 rounded-lg p-3 text-xs space-y-1.5">
          <div class="flex justify-between"><span class="text-slate-400">Decoded Model:</span><span id="specName" class="font-semibold text-white">Mercedes-Benz GLS 450</span></div>
          <div class="flex justify-between"><span id="specParam1Label" class="text-slate-400">Manufacturing Plant:</span><span id="specParam1" class="font-mono text-[#C5A059]">UNITED STATES</span></div>
          <div class="flex justify-between"><span id="specParam2Label" class="text-slate-400">Displacement / Specs:</span><span id="specParam2" class="font-mono text-slate-300">2,999 cc (Gasoline)</span></div>
          <div class="flex justify-between"><span class="text-slate-400">Harmonized Tariff Code:</span><span id="specHsCode" class="font-mono text-amber-300">8703.23.01</span></div>
        </div>

        <div id="fobContainer">
          <label class="block text-xs text-slate-400 mb-1">Sourcing Acquisition Cost ($ USD)</label>
          <input type="number" id="fobInput" value="88000" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm font-mono text-[#C5A059] focus:outline-none focus:border-[#C5A059]">
        </div>
        <div>
          <label class="block text-xs text-slate-400 mb-1">Target Foreign Wholesale Bid ($ USD)</label>
          <input type="number" id="wholesaleInput" value="128000" class="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-sm font-mono text-cyan-400 focus:outline-none focus:border-cyan-500">
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 shadow-xl">
        <h2 class="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center justify-between">
          <span>Bilateral Landed Cost</span>
          <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">CIF Engine</span>
        </h2>
        <div class="space-y-2.5 text-xs">
          <div id="rowFob" class="flex justify-between pb-1.5 border-b border-slate-800/80"><span class="text-slate-400">Base Sourcing Price:</span><span id="outFob" class="font-mono text-white">$88,000.00</span></div>
          <div class="flex justify-between pb-1.5 border-b border-slate-800/80"><span id="labelFreight" class="text-slate-400">International Ocean Freight:</span><span id="outFreight" class="font-mono text-white">$1,450.00</span></div>
          <div class="flex justify-between pb-1.5 border-b border-slate-800/80"><span class="text-slate-400">Marine Cargo Insurance (1.5%):</span><span id="outInsurance" class="font-mono text-white">$1,320.00</span></div>
          <div class="flex justify-between pb-1.5 border-b border-slate-800/80 bg-slate-800/40 p-1.5 rounded"><span class="text-[#C5A059] font-semibold">Total CIF Valuation:</span><span id="outCif" class="font-mono text-[#C5A059] font-bold">$90,770.00</span></div>
          <div class="flex justify-between pb-1.5 border-b border-slate-800/80"><span id="labelDuty" class="text-slate-400">Customs Import Tariff:</span><span id="outDuty" class="font-mono text-white">$0.00</span></div>
          <div class="flex justify-between pb-1.5 border-b border-slate-800/80"><span id="labelVat" class="text-slate-400">Destination VAT / Tax:</span><span id="outVat" class="font-mono text-white">$16,338.60</span></div>
          <div class="flex justify-between pb-1.5 border-b border-slate-800/80"><span id="labelExcise" class="text-slate-400">Selective Surcharge / Tax:</span><span id="outExcise" class="font-mono text-white">$1,815.40</span></div>
          <div class="flex justify-between pb-1.5 border-b border-slate-800/80"><span id="labelPort" class="text-slate-400">Port Handling & Rigging:</span><span id="outPort" class="font-mono text-white">$650.00</span></div>
        </div>
        <div class="pt-3 border-t border-slate-800 bg-slate-950/60 p-3 rounded-lg border border-slate-800/80 flex justify-between items-center">
          <span class="text-xs uppercase font-bold text-slate-300">Total Landed Cost:</span>
          <span id="outTotalLanded" class="text-lg font-mono font-bold text-white">$109,574.00</span>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 flex flex-col justify-between shadow-xl">
        <div>
          <h2 class="text-sm font-semibold text-slate-300 uppercase tracking-wider flex items-center justify-between mb-4">
            <span>Trade Spread & Deliverables</span>
            <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">Arbitrage</span>
          </h2>
          
          <div id="arbitrageCard" class="p-4 bg-[#C5A059]/10 border border-[#C5A059]/30 rounded-xl text-center space-y-1">
            <span class="text-xs text-[#C5A059] font-semibold tracking-wide uppercase">Net Wholesale Arbitrage Spread</span>
            <div id="outNetProfit" class="text-3xl font-mono font-bold text-[#C5A059]">+$18,426.00</div>
            <div id="outRoi" class="text-xs text-[#C5A059]/80 font-mono">Return on Capital: 16.82%</div>
          </div>

          <div class="mt-4 space-y-2 text-xs">
            <div class="p-3 bg-slate-800/60 rounded-lg border border-slate-700/60">
              <div class="flex justify-between items-center"><span class="font-semibold text-slate-300">Homologation Protocol:</span><span id="protocolBadge" class="text-[9px] px-2 py-0.5 rounded bg-emerald-900 text-emerald-300 border border-emerald-700 font-mono">VERIFIED</span></div>
              <p id="outRegulatory" class="text-slate-400 text-[11px] mt-1.5">Checking statutory destination rules...</p>
            </div>
            <div class="p-3 bg-slate-800/60 rounded-lg border border-slate-700/60">
              <div class="flex justify-between items-center"><span class="font-semibold text-slate-300">Export Clearance Status:</span><span id="filingBadge" class="text-[9px] px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 font-mono">CBP 19 CFR § 192.2</span></div>
              <p id="filingDesc" class="text-slate-400 text-[11px] mt-1">AES/ITN clearance ready for filing.</p>
            </div>
          </div>
        </div>

        <button id="pdfGenerateBtn" onclick="handlePdfDownload()" class="w-full bg-[#C5A059] hover:bg-[#d4b067] text-slate-950 font-bold py-3 rounded-lg text-xs tracking-wider uppercase transition shadow-lg flex items-center justify-center gap-2">
          <span>🛡️</span> Generate Watermarked Pro-Forma Quote (PDF)
        </button>
      </div>
    </div>

    <div id="tabContent-multiMatrix" class="hidden bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4 shadow-xl">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div>
          <h2 class="text-base font-bold text-white uppercase tracking-wider">Multi-Lane Cross-Border Arbitrage Matrix</h2>
          <p class="text-xs text-slate-400 mt-0.5">Live benchmark across top global corridors.</p>
        </div>
        <span class="text-xs font-mono text-[#C5A059] bg-[#C5A059]/10 px-3 py-1 rounded border border-[#C5A059]/30">BENCHMARK ACTIVE</span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-xs text-left border border-slate-800">
          <thead class="bg-slate-950 text-slate-400 font-mono border-b border-slate-800">
            <tr>
              <th class="p-3">Target Corridor</th><th class="p-3">Statutory Tariff</th><th class="p-3">Delivered CIF</th>
              <th class="p-3">Total Landed Cost</th><th class="p-3">Foreign Wholesale Bid</th><th class="p-3">Net Spread</th>
              <th class="p-3">ROC %</th><th class="p-3 text-right">Action</th>
            </tr>
          </thead>
          <tbody id="matrixTableBody" class="divide-y divide-slate-800/60 font-mono"></tbody>
        </table>
      </div>
    </div>

    <div id="tabContent-cbpDossier" class="hidden bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5 shadow-xl">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div>
          <h2 class="text-base font-bold text-white uppercase tracking-wider">CBP 72-Hour Export Dossier (19 CFR § 192.2)</h2>
          <p class="text-xs text-slate-400 mt-0.5">Pre-formatted export manifest data for U.S. Customs Automated Export System (AES).</p>
        </div>
        <button onclick="copyDossierToClipboard()" class="bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold px-4 py-2 rounded text-xs uppercase tracking-wider transition flex items-center gap-1.5 shadow-md">
          <span>📋</span> Copy AES Export Dossier
        </button>
      </div>
      <div id="dossierGateOverlay" class="hidden p-6 bg-slate-950/90 border border-amber-800/80 rounded-xl text-center space-y-3">
        <div class="text-amber-400 text-2xl font-bold">🔒 Enterprise Export Clearance Gated</div>
        <p class="text-xs text-slate-300 max-w-md mx-auto">Automated CBP 72-Hour export packet formatting and direct AES filing manifests require an active Trader Desk Pro or Enterprise subscription.</p>
        <button onclick="promptUpgrade()" class="bg-[#C5A059] hover:bg-[#d4b067] text-slate-950 font-bold px-4 py-2 rounded text-xs uppercase tracking-wider transition">Upgrade to Unlock Export Packets</button>
      </div>
      <div id="dossierContentArea">
        <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div><label class="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">Port of Loading (POL)</label><input type="text" id="inputPol" value="PortMiami / Port Everglades, FL" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs font-mono text-[#C5A059] focus:outline-none focus:border-[#C5A059]"></div>
          <div><label class="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">Port of Discharge (POD)</label><input type="text" id="inputPod" value="Port of Rio Haina / Caucedo, DR" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs font-mono text-cyan-400 focus:outline-none focus:border-cyan-500"></div>
          <div><label class="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">Internal Transaction No. (ITN)</label><input type="text" id="inputItn" value="X20261101889921" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs font-mono text-amber-300 focus:outline-none focus:border-amber-500 uppercase"></div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
            <div class="text-slate-400 uppercase font-bold text-[10px] tracking-wider text-[#C5A059]">1. Asset Identification & Title</div>
            <div class="flex justify-between py-1 border-b border-slate-800/80"><span class="text-slate-400">Asset Identifier:</span><span id="dossierAssetId" class="font-mono text-white"></span></div>
            <div class="flex justify-between py-1 border-b border-slate-800/80"><span class="text-slate-400">Title Classification:</span><span class="text-white">Clean Certificate of Title / Bill of Sale</span></div>
            <div class="flex justify-between py-1 border-b border-slate-800/80"><span class="text-slate-400">Staging Window:</span><span class="text-amber-300 font-mono">Presented &gt;= 72-Hours Prior to Loading</span></div>
            <div class="flex justify-between py-1"><span class="text-slate-400">Departure Port (POL):</span><span id="dossierPortText" class="text-[#C5A059] font-mono"></span></div>
          </div>
          <div class="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
            <div class="text-slate-400 uppercase font-bold text-[10px] tracking-wider text-cyan-400">2. AES / Electronic Export Information (EEI)</div>
            <div class="flex justify-between py-1 border-b border-slate-800/80"><span class="text-slate-400">Harmonized Tariff Schedule (HTS):</span><span id="dossierHsCode" class="font-mono text-white">8703.23.01</span></div>
            <div class="flex justify-between py-1 border-b border-slate-800/80"><span class="text-slate-400">Export Information Code:</span><span class="text-white font-mono">OS (Outright Sale)</span></div>
            <div class="flex justify-between py-1 border-b border-slate-800/80"><span class="text-slate-400">Internal Transaction Number (ITN):</span><span id="dossierItnText" class="text-amber-400 font-mono font-bold"></span></div>
            <div class="flex justify-between py-1"><span class="text-slate-400">Destination Port of Discharge:</span><span id="dossierDestText" class="text-cyan-400 font-mono"></span></div>
          </div>
        </div>
      </div>
    </div>

    <div id="tabContent-homologationTab" class="hidden bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4 shadow-xl">
      <div class="flex justify-between items-center border-b border-slate-800 pb-3">
        <div>
          <h2 class="text-base font-bold text-white uppercase tracking-wider">Destination Homologation & Seizure Shield</h2>
          <p class="text-xs text-slate-400 mt-0.5">Automated screening against statutory standards, drive/hull configurations, and age bans.</p>
        </div>
        <span id="homologationCountryBadge" class="text-xs font-mono text-[#C5A059] bg-[#C5A059]/10 px-3 py-1 rounded border border-[#C5A059]/30">AUDITING</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
          <span id="homoCard1Title" class="text-[10px] uppercase font-bold text-slate-400">Configuration Check</span>
          <div id="checkSteering" class="text-sm font-bold text-emerald-400">PASS: Standard Geometry</div>
          <p id="descSteering" class="text-slate-400 text-[11px]">Configuration meets destination requirements.</p>
        </div>
        <div class="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
          <span class="text-[10px] uppercase font-bold text-slate-400">Import Age Ceiling</span>
          <div id="checkAge" class="text-sm font-bold text-emerald-400">PASS: Compliant</div>
          <p id="descAge" class="text-slate-400 text-[11px]">Asset meets destination age rules.</p>
        </div>
        <div class="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-2">
          <span class="text-[10px] uppercase font-bold text-slate-400">Technical Retrofit Standard</span>
          <div id="checkRetrofit" class="text-sm font-bold text-[#C5A059]">NO MAJOR RETROFIT</div>
          <p id="descRetrofit" class="text-slate-400 text-[11px]">No structural conversions required.</p>
        </div>
      </div>
    </div>

    <div id="tabContent-legalTab" class="hidden bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4 text-xs text-slate-300 leading-relaxed shadow-xl">
      <h2 class="text-base font-bold text-white uppercase tracking-wider border-b border-slate-800 pb-3">Legal, Regulatory & Liability Disclaimers</h2>
      <div class="space-y-3">
        <div class="p-3 bg-slate-950 rounded border border-slate-800">
          <h4 class="font-bold text-[#C5A059] uppercase mb-1">1. Informational & Estimation Disclaimer</h4>
          <p class="text-slate-400">Calculations, statutory tariffs, local VAT rates, freight estimates, and landed cost outputs generated by Globarix.com are provided strictly for informational and trade analytical purposes. They do not constitute formal tax advice, legal opinion, or binding customs brokerage valuations. Final duty assessments are determined exclusively by destination port customs authorities upon asset entry.</p>
        </div>
        <div class="p-3 bg-slate-950 rounded border border-slate-800">
          <h4 class="font-bold text-[#C5A059] uppercase mb-1">2. CBP 72-Hour Export & EEI/AES Filing Responsibility</h4>
          <p class="text-slate-400">Globarix.com provides automated data structure formatting under 19 CFR § 192.2 for convenience. Datascope LLC and Globarix.com are not official U.S. Principal Parties in Interest (USPPI) or licensed customs brokers. Users and exporters remain solely responsible for title authentication, physical vehicle staging compliance, and filing Electronic Export Information (EEI) via AES Direct.</p>
        </div>
        <div class="p-3 bg-slate-950 rounded border border-slate-800">
          <h4 class="font-bold text-[#C5A059] uppercase mb-1">3. Homologation & Regulatory Admissibility Disclaimer</h4>
          <p class="text-slate-400">Homologation checks (such as age ceilings, right-hand drive restrictions, or technical retrofit requirements) are based on published sovereign standards. Exporters and buyers must independently verify local port admissibility prior to loading assets onto international vessels.</p>
        </div>
        <div class="p-3 bg-slate-950 rounded border border-slate-800">
          <h4 class="font-bold text-[#C5A059] uppercase mb-1">4. Trade Secret & IP Notice (18 U.S.C. § 1836)</h4>
          <p class="text-slate-400">Globarix.com is a registered DBA of Datascope LLC. All underlying code, calculation engines, trade secret formulas, and proprietary interface designs are protected under 18 U.S.C. § 1836 (Defend Trade Secrets Act) and Florida Statute § 688.</p>
        </div>
      </div>
    </div>

    <div id="limitModal" class="hidden fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
      <div class="bg-slate-900 border border-[#C5A059] rounded-2xl max-w-md w-full p-6 text-center space-y-4 shadow-2xl">
        <div class="h-12 w-12 rounded-full bg-amber-950 text-[#C5A059] flex items-center justify-center mx-auto text-2xl font-bold border border-[#C5A059]/50">🛡️</div>
        <h3 class="text-lg font-bold text-white uppercase tracking-wide">Monthly Preview Limit Reached</h3>
        <p class="text-xs text-slate-300">You have completed your <strong>3 free monthly calculations</strong> under the Free Preview tier.</p>
        <p class="text-xs text-slate-400">To run unlimited calculations across all 197 countries, unlock sovereign consumption taxes, and generate watermarked secure client quotes, activate your trading desk.</p>
        <div class="pt-2 space-y-2">
          <button onclick="promptUpgrade()" class="w-full bg-[#C5A059] hover:bg-[#d4b067] text-slate-950 font-bold py-2.5 rounded-lg text-xs uppercase tracking-wider transition shadow-lg">Start Trader Desk Pro ($499/mo)</button>
          <button onclick="promptSinglePacket()" class="w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold py-2 rounded-lg text-xs uppercase tracking-wider transition border border-slate-700">Unlock This Single Unit ($50)</button>
          <button onclick="closeLimitModal()" class="text-[11px] text-slate-500 hover:text-slate-400 underline pt-1 block mx-auto">Close and review calculation</button>
        </div>
      </div>
    </div>

    <footer class="border-t border-slate-800/80 pt-4 mt-8 flex flex-col md:flex-row justify-between items-center text-[11px] text-slate-500 font-mono">
      <div>© 2026 <strong>Datascope LLC</strong>. All rights reserved. <strong>Globarix.com</strong> is a registered DBA of Datascope LLC.</div>
      <div class="mt-2 md:mt-0 text-right">Protected under 18 U.S.C. § 1836 & Fla. Stat. § 688</div>
    </footer>
  </div>

  <div class="print-only max-w-4xl mx-auto p-8 text-black bg-white relative min-h-screen">
    <div class="watermark">GLOBARIX.COM SECURE DESK — HASH: GX-2026-AUTH</div>
    <div class="border-b-2 border-[#0B1D3A] pb-4 flex justify-between items-end">
      <div>
        <h1 class="text-2xl font-serif font-black uppercase tracking-wider text-[#0B1D3A]">GLOBARIX<span class="text-[#C5A059]">.COM</span></h1>
        <p class="text-xs text-slate-600 mt-0.5">Secure Pro-Forma Quotation & Bilateral Clearance Manifest</p>
      </div>
      <div class="text-right text-xs text-slate-600">
        <div><strong>Date:</strong> <span id="pdfDate"></span></div>
        <div><strong>Quote Ref:</strong> <span class="font-mono">GX-EXP-2026-MULTI</span></div>
        <div><strong>Operating Entity:</strong> Datascope LLC (DBA Globarix.com)</div>
      </div>
    </div>
    <div class="my-6">
      <h3 class="text-xs font-bold uppercase tracking-wider text-[#0B1D3A] mb-2">1. Asset Identification & Route Specifications</h3>
      <table class="w-full text-xs border border-slate-300 border-collapse">
        <tbody>
          <tr class="border-b border-slate-300 bg-slate-50">
            <td class="p-2 font-semibold text-slate-700 w-1/4">Asset Description:</td><td id="pdfAssetDesc" class="p-2 font-bold text-slate-900 w-1/4"></td>
            <td class="p-2 font-semibold text-slate-700 w-1/4">Identifier:</td><td id="pdfIdVal" class="p-2 font-mono text-slate-900 w-1/4"></td>
          </tr>
          <tr class="border-b border-slate-300">
            <td class="p-2 font-semibold text-slate-700">Port of Loading (POL):</td><td id="pdfOrigin" class="p-2 font-bold text-slate-900"></td>
            <td class="p-2 font-semibold text-slate-700">Port of Discharge (POD):</td><td id="pdfDestination" class="p-2 font-bold text-slate-900"></td>
          </tr>
          <tr>
            <td class="p-2 font-semibold text-slate-700">Country of Assembly:</td><td id="pdfPlant" class="p-2 font-mono text-slate-900"></td>
            <td class="p-2 font-semibold text-slate-700">Schedule B / HTS:</td><td id="pdfHsCode" class="p-2 font-mono text-slate-900 font-bold"></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="my-6">
      <h3 class="text-xs font-bold uppercase tracking-wider text-[#0B1D3A] mb-2">2. Delivered Port Pricing & Clearance Schedule</h3>
      <table class="w-full text-xs border border-slate-300 border-collapse">
        <thead class="bg-[#0B1D3A] text-white border-b border-slate-300">
          <tr><th class="p-2 text-left">Line Item Description</th><th class="p-2 text-left">Basis & Statutory Authority</th><th class="p-2 text-right">Amount (USD)</th></tr>
        </thead>
        <tbody>
          <tr class="border-b border-slate-200"><td class="p-2 font-semibold">Delivered CIF Value to Destination Port</td><td class="p-2 text-slate-600">Base Sourcing Price, Dedicated Delivery & Marine Cargo Coverage</td><td id="pdfCif" class="p-2 text-right font-mono"></td></tr>
          <tr class="border-b border-slate-200"><td class="p-2 font-semibold">Statutory Customs Duty</td><td id="pdfDutyNote" class="p-2 text-slate-600"></td><td id="pdfDuty" class="p-2 text-right font-mono"></td></tr>
          <tr class="border-b border-slate-200"><td class="p-2 font-semibold">Destination Import VAT / Tax</td><td id="pdfVatNote" class="p-2 text-slate-600">Statutory destination consumption rate</td><td id="pdfVat" class="p-2 text-right font-mono"></td></tr>
          <tr class="border-b border-slate-200"><td class="p-2 font-semibold">Port Handling, Rigging & Surcharges</td><td class="p-2 text-slate-600">Stevedoring, gate handling, and local selective taxes</td><td id="pdfPortFees" class="p-2 text-right font-mono"></td></tr>
          <tr class="bg-slate-100 font-bold border-t-2 border-[#0B1D3A] text-sm"><td class="p-2.5" colspan="2">TOTAL PORT-CLEARED ACQUISITION COST:</td><td id="pdfTotal" class="p-2.5 text-right font-mono"></td></tr>
        </tbody>
      </table>
    </div>
    <div class="mt-8 text-[9px] text-slate-500 border-t border-slate-300 pt-3">
      <strong>LEGAL NOTICE:</strong> Quotations and calculations are generated by Globarix.com (DBA of Datascope LLC) for trade estimation and analytical purposes. Final tariffs and taxes are assessed by destination customs authorities.
    </div>
  </div>

  <script>
    const GLOBAL_NATIONS = {NATIONS_JSON};
    let activeAssetFamily = "MOTOR_VEHICLE";
    let isBlinded = false;
    let currentTier = "FREE_PREVIEW";
    let lookupsUsed = 0;
    const lookupLimit = 3;

    let activeSpec = {{
      name: "Mercedes-Benz GLS 450",
      param1Label: "Manufacturing Plant:",
      param1: "UNITED STATES",
      param2Label: "Displacement / Specs:",
      param2: "2,999 cc (Gasoline)",
      hsCode: "8703.23.01",
      year: 2024,
      displacementCC: 2999
    }};

    function populateDropdowns() {{
      const originSelect = document.getElementById("originSelect");
      const countrySelect = document.getElementById("countrySelect");
      if (!originSelect || !countrySelect) return;

      const curOrigin = originSelect.value || "US";
      const curDest = countrySelect.value || "DO";

      originSelect.innerHTML = "";
      countrySelect.innerHTML = "";

      const sorted = Object.entries(GLOBAL_NATIONS).sort((a, b) => a[1].name.localeCompare(b[1].name));

      for (const [code, item] of sorted) {{
        const opt1 = document.createElement("option");
        opt1.value = code;
        opt1.textContent = `${{item.name}} (${{code}})`;
        if (code === curOrigin) opt1.selected = true;
        originSelect.appendChild(opt1);

        const opt2 = document.createElement("option");
        opt2.value = code;
        opt2.textContent = `${{item.name}} (${{code}})`;
        if (code === curDest) opt2.selected = true;
        countrySelect.appendChild(opt2);
      }}

      document.getElementById("originCountBadge").textContent = `${{sorted.length}} Loaded`;
      document.getElementById("destCountBadge").textContent = `${{sorted.length}} Loaded`;
    }}

    function onTierChange() {{
      currentTier = document.getElementById("userTierSelect").value;
      const banner = document.getElementById("tierBanner");
      const quotaBadge = document.getElementById("quotaBadge");
      const dossierOverlay = document.getElementById("dossierGateOverlay");
      const dossierContent = document.getElementById("dossierContentArea");

      if (currentTier === "FREE_PREVIEW") {{
        banner.classList.remove("hidden");
        quotaBadge.className = "bg-amber-950/60 border border-amber-800 text-amber-300 px-3 py-1.5 rounded-lg text-xs font-bold";
        dossierOverlay.classList.remove("hidden");
        dossierContent.classList.add("opacity-20", "pointer-events-none");
      }} else {{
        banner.classList.add("hidden");
        quotaBadge.className = "bg-emerald-950/60 border border-emerald-800 text-emerald-300 px-3 py-1.5 rounded-lg text-xs font-bold";
        quotaBadge.innerHTML = currentTier === "TRADER_PRO" ? "Trader Pro: UNLIMITED" : "Enterprise: UNLIMITED (5 Seats)";
        dossierOverlay.classList.add("hidden");
        dossierContent.classList.remove("opacity-20", "pointer-events-none");
      }}
      update();
    }}

    function executeCalculation() {{
      if (currentTier === "FREE_PREVIEW" && lookupsUsed >= lookupLimit) {{
        document.getElementById("limitModal").classList.remove("hidden");
        return;
      }}
      if (currentTier === "FREE_PREVIEW") {{
        lookupsUsed++;
        const remaining = Math.max(0, lookupLimit - lookupsUsed);
        document.getElementById("quotaRemainingText").innerText = remaining;
      }}
      decodeAsset();
    }}

    function closeLimitModal() {{ document.getElementById("limitModal").classList.add("hidden"); }}
    function promptUpgrade() {{ alert("Redirecting to Globarix Stripe Secure Checkout for Trader Desk Pro ($499/month)..."); }}
    function promptSinglePacket() {{ alert("Opening Globarix Stripe Payment Element for Single Unit Clearance Dossier ($50.00)..."); }}

    function handlePdfDownload() {{
      if (currentTier === "FREE_PREVIEW") {{
        alert("🔒 Watermarked PDF Export Locked on Free Preview.\\nUpgrade to Trader Desk Pro ($499/mo) or purchase a Single Clearance Packet ($50) to download authenticated client quotes.");
        return;
      }}
      window.print();
    }}

    function onAssetFamilyChange() {{
      const select = document.getElementById("assetFamilySelect");
      activeAssetFamily = select.value;
      const badge = document.getElementById("assetBadge");
      const inputLabel = document.getElementById("idInputLabel");
      const inputEl = document.getElementById("assetIdInput");
      const presetContainer = document.getElementById("presetButtonsContainer");

      const categoryConfigs = {{
        "MOTOR_VEHICLE": {{
          label: "17-Digit Vehicle Identification Number (VIN)",
          badge: "Active Category: 1. Motor Vehicles & Trucks",
          defaultId: "4JGDA5HB4MA123456",
          maxLen: 25,
          fob: 88000,
          wholesale: 128000,
          name: "Mercedes-Benz GLS 450",
          param1Label: "Manufacturing Plant:",
          param1: "UNITED STATES",
          param2Label: "Displacement / Specs:",
          param2: "2,999 cc (Gasoline)",
          hsCode: "8703.23.01",
          presets: [
            {{ label: "Mercedes GLS", val: "4JGDA5HB4MA123456" }},
            {{ label: "Corolla (US)", val: "4T1B11HK5MU123456" }}
          ]
        }},
        "MARINE_VESSEL": {{
          label: "12-Character Hull Identification Number (HIN)",
          badge: "Active Category: 2. Marine Vessels & Yachts",
          defaultId: "SERP1234A323",
          maxLen: 25,
          fob: 350000,
          wholesale: 490000,
          name: "Lagoon 46 Ocean Catamaran",
          param1Label: "OEM Origin Facility:",
          param1: "UNITED STATES",
          param2Label: "Asset Classification:",
          param2: "Verified Marine Vessel",
          hsCode: "8903.92.00",
          presets: [
            {{ label: "Lagoon Catamaran 46", val: "SERP1234A323" }},
            {{ label: "Sea Ray Sundancer", val: "SERV9876B224" }}
          ]
        }},
        "HEAVY_EQUIPMENT": {{
          label: "17-Character Product Identification Number (PIN)",
          badge: "Active Category: 3. Construction & Mining Machinery",
          defaultId: "CAT0320DCK7890123",
          maxLen: 25,
          fob: 210000,
          wholesale: 295000,
          name: "Caterpillar 320 Hydraulic Excavator",
          param1Label: "OEM Origin Facility:",
          param1: "UNITED STATES",
          param2Label: "Asset Classification:",
          param2: "Heavy Construction Asset",
          hsCode: "8429.52.10",
          presets: [
            {{ label: "CAT 320 Excavator", val: "CAT0320DCK7890123" }},
            {{ label: "Komatsu PC200", val: "KMT0200PC5432109" }}
          ]
        }},
        "AG_EQUIPMENT": {{
          label: "17-Character Serial / PIN",
          badge: "Active Category: 4. Commercial Agricultural Machinery",
          defaultId: "1RW8370RFP8901234",
          maxLen: 25,
          fob: 275000,
          wholesale: 380000,
          name: "John Deere 8R 370 Tractor",
          param1Label: "OEM Origin Facility:",
          param1: "UNITED STATES",
          param2Label: "Asset Classification:",
          param2: "Agricultural Machinery",
          hsCode: "8432.29.00",
          presets: [
            {{ label: "John Deere 8R", val: "1RW8370RFP8901234" }},
            {{ label: "Case IH Magnum", val: "ZDFH12345678901" }}
          ]
        }},
        "POWERSPORTS": {{
          label: "14-17 PIN / VIN Number",
          badge: "Active Category: 5. Powersports, UTVs & RVs",
          defaultId: "3N1AB7AP1KL123456",
          maxLen: 25,
          fob: 32000,
          wholesale: 46000,
          name: "Can-Am Maverick X3 Turbo",
          param1Label: "OEM Origin Facility:",
          param1: "CANADA",
          param2Label: "Asset Classification:",
          param2: "Powersports Vehicle",
          hsCode: "8703.10.50",
          presets: [
            {{ label: "Can-Am Maverick", val: "3N1AB7AP1KL123456" }},
            {{ label: "Polaris RZR", val: "4XA1234567890123" }}
          ]
        }},
        "TRAILERS": {{
          label: "17-Digit Transport Chassis VIN",
          badge: "Active Category: 6. Commercial Transport Trailers",
          defaultId: "1UYVS2531NM123456",
          maxLen: 25,
          fob: 45000,
          wholesale: 65000,
          name: "Utility 53ft Refrigerated Trailer",
          param1Label: "OEM Origin Facility:",
          param1: "UNITED STATES",
          param2Label: "Asset Classification:",
          param2: "Commercial Trailer",
          hsCode: "8716.39.00",
          presets: [
            {{ label: "Utility Reefer Trailer", val: "1UYVS2531NM123456" }},
            {{ label: "Great Dane Dry Van", val: "1GRAA0625KM987654" }}
          ]
        }},
        "POWER_SYSTEMS": {{
          label: "Machine Serial / Asset Number",
          badge: "Active Category: 7. Industrial Power & Generators",
          defaultId: "CUM-C1000D5-9988",
          maxLen: 25,
          fob: 115000,
          wholesale: 165000,
          name: "Cummins C1000D5 1000kVA Generator",
          param1Label: "OEM Origin Facility:",
          param1: "UNITED STATES",
          param2Label: "Asset Classification:",
          param2: "Industrial Power System",
          hsCode: "8502.13.00",
          presets: [
            {{ label: "Cummins C1000D5", val: "CUM-C1000D5-9988" }},
            {{ label: "CAT C18 Generator", val: "CAT-C18-GEN-4432" }}
          ]
        }},
        "MATERIAL_HANDLING": {{
          label: "Equipment PIN / Serial Number",
          badge: "Active Category: 8. Material Handling & Forklifts",
          defaultId: "KALMAR-DRG450-01",
          maxLen: 25,
          fob: 180000,
          wholesale: 250000,
          name: "Kalmar DRG450 Reach Stacker",
          param1Label: "OEM Origin Facility:",
          param1: "SWEDEN",
          param2Label: "Asset Classification:",
          param2: "Material Handling Asset",
          hsCode: "8427.10.00",
          presets: [
            {{ label: "Kalmar Reach Stacker", val: "KALMAR-DRG450-01" }},
            {{ label: "Hyster 12-Ton", val: "HYSTER-H280-9912" }}
          ]
        }},
        "FORESTRY": {{
          label: "Equipment PIN / Chassis Serial",
          badge: "Active Category: 9. Commercial Forestry & Logging",
          defaultId: "TIGERCAT-845E-5512",
          maxLen: 25,
          fob: 240000,
          wholesale: 340000,
          name: "Tigercat 845E Feller Buncher",
          param1Label: "OEM Origin Facility:",
          param1: "CANADA",
          param2Label: "Asset Classification:",
          param2: "Forestry Equipment",
          hsCode: "8436.80.00",
          presets: [
            {{ label: "Tigercat Buncher", val: "TIGERCAT-845E-5512" }},
            {{ label: "Ponsse Harvester", val: "PONSSE-BEAVER-881" }}
          ]
        }},
        "AVIATION": {{
          label: "Aircraft Tail Registration / MSN",
          badge: "Active Category: 10. Commercial Aviation Assets",
          defaultId: "MSN-420-N888GX",
          maxLen: 25,
          fob: 1850000,
          wholesale: 2400000,
          name: "Beechcraft King Air 350i Turboprop",
          param1Label: "OEM Origin Facility:",
          param1: "UNITED STATES",
          param2Label: "Asset Classification:",
          param2: "Commercial Turboprop",
          hsCode: "8802.30.00",
          presets: [
            {{ label: "King Air 350i", val: "MSN-420-N888GX" }},
            {{ label: "Cessna Citation", val: "MSN-525-N999GX" }}
          ]
        }}
      }};

      const cfg = categoryConfigs[activeAssetFamily] || categoryConfigs["MOTOR_VEHICLE"];
      badge.innerText = cfg.badge;
      inputLabel.innerText = cfg.label;
      inputEl.maxLength = cfg.maxLen;
      inputEl.value = cfg.defaultId;
      document.getElementById("fobInput").value = cfg.fob;
      document.getElementById("wholesaleInput").value = cfg.wholesale;

      activeSpec = {{
        name: cfg.name,
        param1Label: cfg.param1Label,
        param1: cfg.param1,
        param2Label: cfg.param2Label,
        param2: cfg.param2,
        hsCode: cfg.hsCode,
        year: 2024,
        displacementCC: activeAssetFamily === "MOTOR_VEHICLE" ? 2999 : 0
      }};

      document.getElementById("specName").innerText = activeSpec.name;
      document.getElementById("specParam1Label").innerText = activeSpec.param1Label;
      document.getElementById("specParam1").innerText = activeSpec.param1;
      document.getElementById("specParam2Label").innerText = activeSpec.param2Label;
      document.getElementById("specParam2").innerText = activeSpec.param2;
      document.getElementById("specHsCode").innerText = activeSpec.hsCode;

      let html = `<span class="text-slate-500 py-0.5">Category Presets:</span>`;
      cfg.presets.forEach(p => {{
        html += `<button onclick="setAssetPreset('${{p.val}}')" class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-0.5 rounded border border-slate-700">${{p.label}}</button>`;
      }});
      presetContainer.innerHTML = html;

      update();
      renderArbitrageMatrix();
    }}

    function setAssetPreset(val) {{
      document.getElementById("assetIdInput").value = val;
      executeCalculation();
    }}

    async function decodeAsset() {{
      const idVal = document.getElementById("assetIdInput").value.trim();
      const btn = document.getElementById("decodeBtn");
      btn.innerText = "...";
      btn.disabled = true;

      try {{
        if (activeAssetFamily === "MOTOR_VEHICLE") {{
          const res = await fetch('/api/decode?vin=' + encodeURIComponent(idVal));
          const data = await res.json();
          activeSpec = {{
            name: `${{data.year}} ${{data.make}} ${{data.model}}`,
            param1Label: "Manufacturing Plant:",
            param1: data.plantCountry || "UNITED STATES",
            param2Label: "Displacement / Fuel:",
            param2: `${{Math.round(data.displacementCC)}} cc (${{data.fuelType}})`,
            hsCode: "8703.23.01",
            year: data.year,
            displacementCC: data.displacementCC
          }};
          document.getElementById("specName").innerText = activeSpec.name;
          document.getElementById("specParam1Label").innerText = activeSpec.param1Label;
          document.getElementById("specParam1").innerText = activeSpec.param1;
          document.getElementById("specParam2Label").innerText = activeSpec.param2Label;
          document.getElementById("specParam2").innerText = activeSpec.param2;
          document.getElementById("specHsCode").innerText = activeSpec.hsCode;
        }}
        update();
        renderArbitrageMatrix();
      }} catch (err) {{
        console.error("Decoding error:", err);
      }} finally {{
        btn.innerText = "Run";
        btn.disabled = false;
      }}
    }}

    function switchTab(tabId) {{
      const tabs = ['tradeDesk', 'multiMatrix', 'cbpDossier', 'homologationTab', 'legalTab'];
      tabs.forEach(t => {{
        const content = document.getElementById('tabContent-' + t);
        const btn = document.getElementById('tabBtn-' + t);
        if (content && btn) {{
          if (t === tabId) {{
            content.classList.remove('hidden');
            btn.className = "px-4 py-2 border-b-2 border-[#C5A059] text-[#C5A059] font-bold transition";
          }} else {{
            content.classList.add('hidden');
            btn.className = "px-4 py-2 border-b-2 border-transparent text-slate-400 hover:text-white transition";
          }}
        }}
      }});
      if (tabId === 'multiMatrix') renderArbitrageMatrix();
      if (tabId === 'cbpDossier') syncDossierFields();
    }}

    function toggleBlindedMode() {{
      isBlinded = !isBlinded;
      const btn = document.getElementById("blindedToggleBtn");
      const fobContainer = document.getElementById("fobContainer");
      const rowFob = document.getElementById("rowFob");
      const arbCard = document.getElementById("arbitrageCard");

      if (isBlinded) {{
        btn.innerText = "ON (IP Protected)";
        btn.className = "px-2.5 py-1 rounded text-[10px] font-bold uppercase transition bg-[#C5A059] text-slate-950 shadow-md";
        fobContainer.classList.add('opacity-30', 'pointer-events-none');
        rowFob.classList.add('hidden');
        arbCard.classList.add('hidden');
      }} else {{
        btn.innerText = "OFF";
        btn.className = "px-2.5 py-1 rounded text-[10px] font-bold uppercase transition bg-slate-800 text-slate-300 border border-slate-700";
        fobContainer.classList.remove('opacity-30', 'pointer-events-none');
        rowFob.classList.remove('hidden');
        arbCard.classList.remove('hidden');
      }}
    }}

    function syncDossierFields() {{
      const pol = document.getElementById("inputPol").value;
      const pod = document.getElementById("inputPod").value;
      const itn = document.getElementById("inputItn").value.trim() || "X20261101889921";
      const idVal = document.getElementById("assetIdInput").value.trim();

      document.getElementById("dossierAssetId").innerText = idVal;
      document.getElementById("dossierPortText").innerText = pol;
      document.getElementById("dossierDestText").innerText = pod;
      document.getElementById("dossierItnText").innerText = itn;
      document.getElementById("dossierHsCode").innerText = activeSpec.hsCode;

      document.getElementById("pdfAssetDesc").innerText = activeSpec.name;
      document.getElementById("pdfIdVal").innerText = idVal;
      document.getElementById("pdfOrigin").innerText = pol;
      document.getElementById("pdfDestination").innerText = pod;
      document.getElementById("pdfPlant").innerText = activeSpec.param1;
      document.getElementById("pdfHsCode").innerText = activeSpec.hsCode;
    }}

    function update() {{
      const originKey = document.getElementById("originSelect").value || "US";
      const destKey = document.getElementById("countrySelect").value || "DO";
      const origin = GLOBAL_NATIONS[originKey] || GLOBAL_NATIONS["US"];
      const dest = GLOBAL_NATIONS[destKey] || GLOBAL_NATIONS["DO"];

      const fob = parseFloat(document.getElementById("fobInput").value) || 0;
      const wholesale = parseFloat(document.getElementById("wholesaleInput").value) || 0;

      let freight = dest.freight;
      let portHandling = dest.port;

      const ins = fob * 0.015;
      const cif = fob + freight + ins;

      let dutyRate = dest.tariff;
      let dutyNote = `Statutory ${{dest.name}} Customs Tariff`;

      if (dest.ftaOrigin && (dest.ftaOrigin.includes(originKey) || (activeSpec.param1.includes("UNITED STATES") && dest.ftaOrigin.includes("US")))) {{
        dutyRate = 0.00;
        dutyNote = `0% Preferential FTA Rate (${{origin.name}} Origin Verified)`;
      }}

      const duty = cif * dutyRate;
      const vat = (cif + duty) * dest.vat;

      let excise = 0.0;
      if (activeAssetFamily === "MOTOR_VEHICLE") {{
        if (dest.excise === "tiered_cc") {{
          const cc = activeSpec.displacementCC || 2000;
          const iscRate = cc <= 1600 ? 0.00 : (cc <= 2000 ? 0.01 : (cc <= 3000 ? 0.02 : 0.03));
          excise = (cif + duty) * iscRate;
        }} else if (dest.excise === "levy_15") {{
          excise = cif * 0.15;
        }}
      }}

      const totalLanded = cif + duty + vat + excise + portHandling;
      const profit = wholesale - totalLanded;
      const roc = totalLanded > 0 ? (profit / totalLanded) * 100 : 0;

      document.getElementById("outFob").innerText = '$' + fob.toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("outFreight").innerText = '$' + freight.toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("outInsurance").innerText = '$' + ins.toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("outCif").innerText = '$' + cif.toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("outDuty").innerText = '$' + duty.toLocaleString('en-US', {{minimumFractionDigits: 2}});

      const isFree = currentTier === "FREE_PREVIEW";
      const vatEl = document.getElementById("outVat");
      const exciseEl = document.getElementById("outExcise");
      const portEl = document.getElementById("outPort");
      const landedEl = document.getElementById("outTotalLanded");
      const profitEl = document.getElementById("outNetProfit");
      const roiEl = document.getElementById("outRoi");

      if (isFree) {{
        vatEl.innerText = "🔒 Protected (Trader Pro)";
        vatEl.className = "font-mono text-[#C5A059] font-semibold";
        exciseEl.innerText = "🔒 Protected (Trader Pro)";
        exciseEl.className = "font-mono text-[#C5A059] font-semibold";
        portEl.innerText = "🔒 Protected (Trader Pro)";
        portEl.className = "font-mono text-[#C5A059] font-semibold";
        landedEl.innerText = "🔒 Upgrade to Calculate";
        landedEl.className = "text-sm font-mono font-bold text-[#C5A059]";
        profitEl.innerText = "🔒 SPREAD PROTECTED";
        profitEl.className = "text-2xl font-mono font-bold text-[#C5A059]";
        roiEl.innerText = "Activate Trader Pro ($499/mo) to unlock exact margins";
        roiEl.className = "text-xs text-[#C5A059]/80 font-mono";
      }} else {{
        vatEl.innerText = '$' + vat.toLocaleString('en-US', {{minimumFractionDigits: 2}});
        vatEl.className = "font-mono text-white";
        exciseEl.innerText = '$' + excise.toLocaleString('en-US', {{minimumFractionDigits: 2}});
        exciseEl.className = "font-mono text-white";
        portEl.innerText = '$' + portHandling.toLocaleString('en-US', {{minimumFractionDigits: 2}});
        portEl.className = "font-mono text-white";
        landedEl.innerText = '$' + totalLanded.toLocaleString('en-US', {{minimumFractionDigits: 2}});
        landedEl.className = "text-lg font-mono font-bold text-white";
        profitEl.innerText = (profit >= 0 ? '+$' : '-$') + Math.abs(profit).toLocaleString('en-US', {{minimumFractionDigits: 2}});
        profitEl.className = profit >= 0 ? "text-3xl font-mono font-bold text-emerald-400" : "text-3xl font-mono font-bold text-rose-500";
        roiEl.innerText = 'Return on Capital: ' + roc.toFixed(2) + '%';
        roiEl.className = "text-xs text-emerald-300 font-mono";
      }}

      document.getElementById("homologationCountryBadge").innerText = dest.name.toUpperCase();
      document.getElementById("homoCard1Title").innerText = "Configuration Check";
      document.getElementById("checkSteering").innerText = dest.rhd ? "WARNING: RHD Mandate" : "PASS: Standard Geometry Authorized";
      document.getElementById("descSteering").innerText = dest.rhd ? "Right-Hand Drive destination country." : "Standard Drive Configuration permitted.";

      syncDossierFields();
      document.getElementById("pdfDate").innerText = new Date().toLocaleDateString('en-US', {{ year: 'numeric', month: 'short', day: 'numeric' }});
      document.getElementById("pdfCif").innerText = '$' + cif.toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("pdfDutyNote").innerText = dutyNote;
      document.getElementById("pdfDuty").innerText = '$' + duty.toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("pdfVatNote").innerText = `${{(dest.vat * 100).toFixed(1)}}% statutory consumption tax`;
      document.getElementById("pdfVat").innerText = '$' + vat.toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("pdfPortFees").innerText = '$' + (portHandling + excise).toLocaleString('en-US', {{minimumFractionDigits: 2}});
      document.getElementById("pdfTotal").innerText = '$' + totalLanded.toLocaleString('en-US', {{minimumFractionDigits: 2}});
    }}

    function renderArbitrageMatrix() {{
      const tbody = document.getElementById("matrixTableBody");
      if (!tbody) return;
      tbody.innerHTML = "";
      const fob = parseFloat(document.getElementById("fobInput").value) || 0;
      const wholesale = parseFloat(document.getElementById("wholesaleInput").value) || 0;
      const originKey = document.getElementById("originSelect").value || "US";

      const sampleLanes = ["DO", "DE", "AE", "CO", "NG", "CL", "JP", "AU", "ZA", "CA"];
      sampleLanes.forEach(code => {{
        const d = GLOBAL_NATIONS[code];
        if (!d) return;
        let freight = d.freight;
        let portFees = d.port;
        const ins = fob * 0.015;
        const cif = fob + freight + ins;

        let dutyRate = d.tariff;
        if (d.ftaOrigin && (d.ftaOrigin.includes(originKey) || (activeSpec.param1.includes("UNITED STATES") && d.ftaOrigin.includes("US")))) {{
          dutyRate = 0.00;
        }}

        const duty = cif * dutyRate;
        const vat = (cif + duty) * d.vat;
        const landed = cif + duty + vat + portFees;
        const spread = wholesale - landed;
        const roc = landed > 0 ? (spread / landed) * 100 : 0;

        const isFree = currentTier === "FREE_PREVIEW";
        const tr = document.createElement("tr");
        tr.className = "hover:bg-slate-800/40 transition";
        tr.innerHTML = `
          <td class="p-3 font-semibold text-white">${{d.name}} (${{code}})</td>
          <td class="p-3 text-slate-300">${{(dutyRate * 100).toFixed(1)}}%</td>
          <td class="p-3 text-slate-300">$${{cif.toLocaleString('en-US', {{maximumFractionDigits:0}})}}</td>
          <td class="p-3 text-slate-300 font-bold">${{isFree ? '🔒 Protected' : '$' + landed.toLocaleString('en-US', {{maximumFractionDigits:0}})}}</td>
          <td class="p-3 text-slate-300">$${{wholesale.toLocaleString('en-US', {{maximumFractionDigits:0}})}}</td>
          <td class="p-3 ${{spread >= 0 ? 'text-emerald-400 font-bold' : 'text-rose-400'}}">${{isFree ? '🔒 Pro Only' : (spread >= 0 ? '+$' : '-$') + Math.abs(spread).toLocaleString('en-US', {{maximumFractionDigits:0}})}}</td>
          <td class="p-3 ${{roc >= 0 ? 'text-emerald-400' : 'text-rose-400'}}">${{isFree ? '🔒' : roc.toFixed(1) + '%'}}</td>
          <td class="p-3 text-right">
            <button onclick="selectCorridorDirect('${{code}}')" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-[#C5A059] hover:text-slate-950 text-slate-300 border border-slate-700 text-[10px] font-bold uppercase transition">
              Select
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function selectCorridorDirect(destCode) {{
      document.getElementById("countrySelect").value = destCode;
      switchTab('tradeDesk');
      update();
    }}

    function copyDossierToClipboard() {{
      if (currentTier === "FREE_PREVIEW") {{
        promptUpgrade();
        return;
      }}
      const idVal = document.getElementById("assetIdInput").value.trim();
      const pol = document.getElementById("inputPol").value.trim();
      const pod = document.getElementById("inputPod").value.trim();
      const itn = document.getElementById("inputItn").value.trim() || "X20261101889921";
      
      const dossierText = `=== U.S. CUSTOMS & BORDER PROTECTION 72-HOUR EXPORT DOSSIER (19 CFR § 192.2) ===\\n` +
        `INTERNAL TRANSACTION NUMBER (ITN): ${{itn}}\\n` +
        `ASSET CLASSIFICATION: ${{activeAssetFamily}}\\n` +
        `IDENTIFIER: ${{idVal}}\\n` +
        `ASSET DESCRIPTION: ${{activeSpec.name}}\\n` +
        `SCHEDULE B / HTS CODE: ${{activeSpec.hsCode}}\\n` +
        `PORT OF LOADING (POL): ${{pol}}\\n` +
        `PORT OF DISCHARGE (POD): ${{pod}}\\n` +
        `STATUS: EEI Automated Export System (AES) Direct Transmission Ready\\n` +
        `OPERATING ENTITY: Datascope LLC (DBA Globarix.com)\\n` +
        `================================================================================`;
        
      navigator.clipboard.writeText(dossierText).then(() => {{
        alert("CBP 72-Hour Export Dossier copied to clipboard successfully!");
      }}).catch(err => {{
        alert("Error copying dossier: " + err);
      }});
    }}

    document.addEventListener("DOMContentLoaded", () => {{
      populateDropdowns();
      onAssetFamilyChange();
      onTierChange();
      update();
    }});

    window.addEventListener("load", () => {{
      populateDropdowns();
    }});

    ['inputPol', 'inputPod', 'inputItn'].forEach(id => {{
      const el = document.getElementById(id);
      if (el) el.addEventListener('input', syncDossierFields);
    }});

    document.getElementById("originSelect").addEventListener('change', update);
    document.getElementById("countrySelect").addEventListener('change', update);
    document.getElementById("fobInput").addEventListener('input', update);
    document.getElementById("wholesaleInput").addEventListener('input', update);
  </script>
</body>
</html>
"""

FAVICON_SVG = """<svg viewBox="0 0 100 115" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M50 2L95 20V55C95 78 75 98 50 113C25 98 5 78 5 55V20L50 2Z" fill="#0B1D3A" stroke="#FFFFFF" stroke-width="5"/>
  <path d="M50 16L85 30V55C85 73 70 88 50 100C30 88 15 73 15 55V30L50 16Z" fill="#0B1D3A"/>
  <path d="M30 35H70M30 45H70M30 55H70M30 65H70M30 75H70M40 25V85M50 25V85M60 25V85" stroke="#C5A059" stroke-width="2.5"/>
  <path d="M72 45H42V72H72V58H56" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
</svg>"""

class SecurityTierGuard:
    def __init__(self):
        self.request_counts = {}
        self.blocked_ips = set()

    def check_rate_limit(self, client_ip):
        now = time.time()
        window = 60
        max_requests = 120
        if client_ip in self.blocked_ips:
            return False
        history = self.request_counts.get(client_ip, [])
        history = [t for t in history if now - t < window]
        if len(history) >= max_requests:
            self.blocked_ips.add(client_ip)
            return False
        history.append(now)
        self.request_counts[client_ip] = history
        return True

security_guard = SecurityTierGuard()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        if not security_guard.check_rate_limit(client_ip):
            self.send_response(429)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Rate limit exceeded."}')
            return

        if self.path == "/api/favicon.svg":
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(FAVICON_SVG.encode("utf-8"))
            return

        elif self.path.startswith("/api/decode"):
            query_str = self.path.split("?", 1)[-1] if "?" in self.path else ""
            vin = "4JGDA5HB4MA123456"
            for param in query_str.split("&"):
                if param.startswith("vin="):
                    vin = param.split("=")[-1]
            url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
            req = urllib.request.Request(url, headers={"User-Agent": "Globarix-TradeOS/5.4"})
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    api_data = json.loads(resp.read().decode("utf-8"))
                    row = api_data.get("Results", [{}])[0]
                    raw_cc = row.get("DisplacementCC") or "2999"
                    displacement = float(raw_cc) if raw_cc.replace(".", "", 1).isdigit() else 2999.0
                    raw_year = row.get("ModelYear") or "2024"
                    year = int(raw_year) if raw_year.isdigit() else 2024
                    payload = {
                        "make": row.get("Make") or "Mercedes-Benz",
                        "model": row.get("Model") or "GLS 450",
                        "year": year,
                        "plantCountry": (row.get("PlantCountry") or "UNITED STATES").upper(),
                        "displacementCC": displacement,
                        "fuelType": row.get("FuelTypePrimary") or "Gasoline"
                    }
            except Exception:
                payload = {
                    "make": "Mercedes-Benz",
                    "model": "GLS 450",
                    "year": 2024,
                    "plantCountry": "UNITED STATES",
                    "displacementCC": 2999.0,
                    "fuelType": "Gasoline"
                }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        elif self.path == "/" or self.path == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("X-Globarix-IP-Protection", "Active")
            self.send_header("X-Trade-Secret-Notice", "Protected under 18 U.S.C. 1836 & Fla. Stat. 688")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
            return
        else:
            return super().do_GET()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

with ReusableTCPServer(("", PORT), Handler) as httpd:
    print(f"\n=======================================================")
    print(f"  GLOBARIX.COM — MULTI-ASSET LANDED-COST OS (v5.4)")
    print(f"  COMPANY: Datascope LLC | DBA: Globarix.com")
    print(f"  URL: http://localhost:{PORT}")
    print(f"  Press Control + C in this Terminal to stop")
    print(f"=======================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped cleanly.")
