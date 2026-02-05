# Business Glossary

**Project:** NYC Green Taxi Analytics  
**Purpose:** Define business terms and metrics for consistent understanding  
**Created:** 2026-02-05  
**Author:** Bianca (BiSemantic)  
**Audience:** Business Analysts, Executives, Operations Teams

---

## Table of Contents

1. [Core Business Concepts](#core-business-concepts)
2. [Financial Metrics](#financial-metrics)
3. [Operational Metrics](#operational-metrics)
4. [Efficiency Metrics](#efficiency-metrics)
5. [Geographic Terms](#geographic-terms)
6. [Regulatory Terms](#regulatory-terms)
7. [Acronyms & Abbreviations](#acronyms--abbreviations)

---

## Core Business Concepts

### Trip
**Definition:** A single taxi journey from pickup location to dropoff location with one or more passengers.  
**Business Owner:** Operations Team  
**Data Source:** `fact_trips`  
**Grain:** One row per trip  

**Related Terms:**
- **Street-hail Trip:** Trip initiated by passenger hailing taxi on street
- **Dispatch Trip:** Trip initiated through app/phone dispatch system
- **Completed Trip:** Trip with valid pickup and dropoff timestamps and payment

---

### Green Taxi (Boro Taxi)
**Definition:** NYC taxis authorized to pick up passengers in outer boroughs (Brooklyn, Queens, Bronx, Staten Island) and upper Manhattan (above 96th St/110th St). Prohibited from street-hails in core Manhattan.  
**Introduced:** 2013  
**Fleet Size:** ~50,000 vehicles  
**Distinguishing Feature:** Green/apple green exterior color  

**Service Zone Rules:**
- ✅ Can pick up: Brooklyn, Queens, Bronx, Staten Island, Upper Manhattan, airports
- ❌ Cannot pick up: Manhattan below 96th/110th St (Yellow Taxi zone)
- ✅ Can drop off: Anywhere in NYC

---

### TLC (Taxi & Limousine Commission)
**Definition:** NYC agency responsible for licensing and regulating taxi and for-hire vehicles.  
**Role:** Regulatory authority, data collection, policy enforcement  
**Website:** nyc.gov/tlc

---

## Financial Metrics

### Total Revenue
**Definition:** Sum of all amounts paid for trips, including fare, extras, taxes, tips, tolls, and surcharges.  
**Formula:** `SUM(total_amount)`  
**Unit:** USD ($)  
**Business Rule:** Excludes voided trips and disputes  
**KPI Target:** N/A (tracking metric)  

**Components:**
- Fare amount (base fare)
- Extra charges (rush hour $0.50, overnight $1.00)
- MTA tax ($0.50 fixed)
- Tips (credit card only)
- Tolls (actual tolls paid)
- Improvement surcharge ($0.30 fixed)
- Congestion surcharge ($2.75 for Manhattan)

---

### Average Revenue Per Trip
**Definition:** Mean revenue generated per completed trip.  
**Formula:** `DIVIDE(SUM(total_amount), COUNT(trips))`  
**Unit:** USD ($)  
**Baseline (Q2/2021):** $12.50  
**Target (Q2/2026):** $14.00  
**Owner:** Sarah Chen (Director of Operations)  

**Interpretation:**
- 🔴 Below $11.00: Critical - investigate pricing or service quality issues
- 🟡 $11.00-$13.00: Monitoring - review for improvement opportunities
- 🟢 Above $13.00: Healthy - meeting or exceeding targets

**Key Drivers:**
- Trip distance (longer = higher revenue)
- Payment type (credit card = tips tracked)
- Time of day (rush hour = extra charges)
- Rate code (airport = premium rates)

---

### Tip Percentage
**Definition:** Tip amount as percentage of base fare.  
**Formula:** `(tip_amount / fare_amount) * 100`  
**Unit:** Percentage (%)  
**Industry Benchmark:** 15-20%  
**Data Limitation:** Only tracked for credit card payments (cash tips unknown)  

**Analysis Notes:**
- Zero tips on cash payments (not tracked, not representative)
- High variation by service quality, customer demographics
- Useful for driver performance evaluation

---

### Revenue Per Mile
**Definition:** Average revenue generated per mile traveled.  
**Formula:** `total_amount / trip_distance`  
**Unit:** USD per mile ($/mi)  
**Typical Range:** $4.00-$8.00  
**Use Case:** Efficiency analysis, route optimization  

**Factors:**
- Rate code (flat rate vs metered)
- Traffic conditions (slower = higher time-based fare)
- Surcharges (congestion, improvement)

---

### Revenue Per Minute
**Definition:** Average revenue generated per minute of trip duration.  
**Formula:** `total_amount / trip_duration_min`  
**Unit:** USD per minute ($/min)  
**Typical Range:** $0.50-$1.50  
**Use Case:** Time utilization, congestion impact analysis  

**Interpretation:**
- Higher values = efficient trips (less idle time)
- Lower values = congestion or inefficient routing

---

## Operational Metrics

### Fleet Utilization Rate
**Definition:** Percentage of time vehicles are actively transporting passengers vs available for hire.  
**Formula:** `SUM(trip_duration) / SUM(shift_duration) * 100`  
**Unit:** Percentage (%)  
**Baseline:** 65%  
**Target:** 80%  
**Owner:** Sarah Chen  

**Calculation Note:** Based on trip duration as proxy; actual shift duration requires driver data (not in current dataset).

---

### Passenger Count
**Definition:** Total number of passengers transported across all trips.  
**Formula:** `SUM(passenger_count)`  
**Unit:** Count  
**Typical Range:** 1-6 per trip (regulatory limit: 5 passengers + driver seat)  
**Average:** ~1.5 passengers per trip  

**Business Use:**
- Capacity planning
- Revenue per passenger calculations
- Service demand forecasting

---

### Trip Distance
**Definition:** Total distance traveled during trip, measured in miles.  
**Unit:** Miles  
**Measurement:** GPS/taximeter  
**Typical Range:** 0.1-50 miles  
**Median:** ~2.5 miles  

**Data Quality Note:** Distances <0.1 miles flagged as potentially erroneous in Silver layer DQ.

---

### Trip Duration
**Definition:** Total time from passenger pickup to dropoff.  
**Formula:** `dropoff_datetime - pickup_datetime`  
**Unit:** Minutes  
**Typical Range:** 5-120 minutes  
**Median:** ~15 minutes  

**Use Cases:**
- Wait time analysis
- Congestion impact studies
- Driver productivity metrics

---

### Average Wait Time
**Definition:** Mean time passengers wait from trip request to pickup.  
**Formula:** `AVG(pickup_datetime - request_datetime)`  
**Unit:** Minutes  
**Baseline:** 12 minutes  
**Target:** 7 minutes  
**Owner:** Jennifer Park (Head of BI)  

**Data Limitation:** Request timestamps not available in current dataset; estimated using trip density patterns.

---

## Efficiency Metrics

### Trip per Driver per Shift
**Definition:** Average number of trips completed by a driver during a work shift.  
**Formula:** `COUNT(trips) / COUNT(DISTINCT drivers)`  
**Typical Range:** 15-25 trips per 8-hour shift  
**Data Availability:** Not available (requires driver dimension - future enhancement)

---

### Occupancy Rate
**Definition:** Percentage of trips with multiple passengers.  
**Formula:** `COUNT(trips WHERE passenger_count > 1) / COUNT(trips) * 100`  
**Unit:** Percentage (%)  
**Industry Average:** ~15-20%  

---

## Geographic Terms

### Borough
**Definition:** One of five administrative divisions of NYC.  
**Values:** Manhattan, Brooklyn, Queens, Bronx, Staten Island  
**Data Source:** `dim_location.borough`  

**Green Taxi Service Rules by Borough:**
- **Manhattan:** Only above 96th St (East) / 110th St (West)
- **Brooklyn, Queens, Bronx, Staten Island:** Full service allowed
- **Airports:** JFK and LaGuardia (full service)

---

### TLC Taxi Zone
**Definition:** Geographic areas defined by NYC TLC for trip tracking and analysis.  
**Total Zones:** 265  
**Data Source:** `dim_location` (from TLC Taxi Zone Shapefile)  
**Zone ID Range:** 1-265  

**Examples:**
- Zone 4: Alphabet City (Manhattan)
- Zone 132: JFK Airport
- Zone 138: LaGuardia Airport
- Zone 237: Upper East Side North

---

### Service Zone
**Definition:** Classification of TLC zones by service type allowed.  

**Types:**
- **Yellow Zone:** Core Manhattan - Yellow Taxis only for street-hail
- **Boro Zone:** Outer boroughs - Green Taxis allowed
- **Airports:** JFK, LaGuardia, Newark - Both allowed
- **EWR (Newark):** Newark Airport (New Jersey)

---

## Regulatory Terms

### Rate Code
**Definition:** Fare calculation method applied to trip.  
**Regulatory Body:** NYC TLC  
**Data Source:** `dim_rate`  

**Standard Rates:**
1. **Standard Rate:** Metered fare (most common)
2. **JFK:** Flat $52 fare + tolls/surcharges
3. **Newark:** Metered + $17.50 surcharge
4. **Nassau/Westchester:** Metered + negotiated surcharge
5. **Negotiated Fare:** Pre-agreed amount
6. **Group Ride:** Shared ride discount

---

### MTA Tax
**Definition:** Fixed tax supporting Metropolitan Transportation Authority.  
**Amount:** $0.50 per trip  
**Applicability:** All metered trips  
**Revenue Destination:** MTA (not driver/fleet revenue)

---

### Improvement Surcharge
**Definition:** Fee funding taxi industry improvements and accessibility.  
**Amount:** $0.30 per trip  
**Introduced:** 2015  
**Use:** Infrastructure, wheelchair-accessible vehicle subsidies

---

### Congestion Surcharge
**Definition:** Fee to reduce traffic congestion in Manhattan core.  
**Amount:** $2.75 per trip  
**Applicability:** Pickups south of 96th St in Manhattan  
**Introduced:** 2019  
**Revenue Destination:** MTA capital projects

---

## Payment Methods

### Credit Card
**Code:** 1  
**Tip Tracking:** Yes (recorded)  
**Fee:** ~2.5% merchant fee (paid by driver/fleet)  
**Adoption:** ~70% of trips

---

### Cash
**Code:** 2  
**Tip Tracking:** No (cash tips not recorded in system)  
**Adoption:** ~25% of trips  
**Data Limitation:** Undermeasures actual tip revenue

---

### No Charge
**Code:** 3  
**Use Cases:** Promotional rides, service recovery, staff transport  
**Revenue Impact:** $0.00

---

### Dispute
**Code:** 4  
**Definition:** Passenger contests charge, under investigation  
**Business Rule:** Excluded from revenue metrics until resolved

---

### Voided Trip
**Code:** 6  
**Definition:** Trip canceled or nullified  
**Business Rule:** Excluded from all metrics

---

## Time-Based Terms

### Rush Hour
**Definition:** Periods of peak traffic and demand.  
**Extra Charge:** $0.50  

**Time Periods:**
- Weekday PM: 4:00 PM - 8:00 PM
- Weekday AM: 6:00 AM - 10:00 AM (varies by location)

---

### Overnight
**Definition:** Late night/early morning period.  
**Extra Charge:** $1.00  
**Time Period:** 8:00 PM - 6:00 AM (varies by TLC regulation)

---

### Weekend
**Definition:** Saturday and Sunday (full day).  
**Data Source:** `dim_date.is_weekend`  
**Impact:** Different demand patterns, higher tips, fewer business trips

---

### Holiday
**Definition:** US Federal holidays.  
**Data Source:** `dim_date.is_holiday`, `dim_date.holiday_name`  
**Examples:** New Year's Day, Independence Day, Thanksgiving, Christmas  
**Impact:** Lower volume, premium fares, altered demand patterns

---

## KPIs (Key Performance Indicators)

### KPI-01: Average Revenue Per Trip
- **Baseline:** $12.50 (Q2/2021)
- **Target:** $14.00 (Q2/2026)
- **Threshold:** 🔴 <$11 | 🟡 $11-$13 | 🟢 >$13
- **Owner:** Sarah Chen

### KPI-02: Fleet Utilization Rate
- **Baseline:** 65%
- **Target:** 80%
- **Threshold:** 🔴 <60% | 🟡 60-75% | 🟢 >75%
- **Owner:** Sarah Chen

### KPI-03: Average Wait Time
- **Baseline:** 12 minutes
- **Target:** 7 minutes
- **Threshold:** 🔴 >15min | 🟡 10-15min | 🟢 <10min
- **Owner:** Jennifer Park

### KPI-04: Data Quality Score
- **Baseline:** 92%
- **Target:** 99%
- **Threshold:** 🔴 <95% | 🟡 95-98% | 🟢 >98%
- **Owner:** Data Engineering Team

### KPI-05: Report Generation Time
- **Baseline:** 5 days
- **Target:** 1 hour
- **Owner:** BI Team

### KPI-06: NPS (Net Promoter Score)
- **Baseline:** 45
- **Target:** 70
- **Owner:** Customer Experience Team

---

## Acronyms & Abbreviations

| Acronym | Full Term | Description |
|---------|-----------|-------------|
| **TLC** | Taxi & Limousine Commission | NYC regulatory authority |
| **MTA** | Metropolitan Transportation Authority | NYC public transit agency |
| **NPS** | Net Promoter Score | Customer satisfaction metric |
| **KPI** | Key Performance Indicator | Critical business metric |
| **YTD** | Year-To-Date | Cumulative from Jan 1 to current date |
| **YoY** | Year-over-Year | Comparison to same period last year |
| **MTD** | Month-To-Date | Cumulative from 1st of month |
| **QoQ** | Quarter-over-Quarter | Comparison to previous quarter |
| **PY** | Prior Year | Previous calendar year |
| **RPM** | Revenue Per Mile | Financial efficiency metric |
| **RPMin** | Revenue Per Minute | Time efficiency metric |
| **ETL** | Extract, Transform, Load | Data pipeline process |
| **DQ** | Data Quality | Data validation and accuracy |
| **SCD** | Slowly Changing Dimension | Dimension change handling strategy |
| **DAX** | Data Analysis Expressions | Power BI formula language |
| **TMDL** | Tabular Model Definition Language | Semantic model definition format |

---

## Business Rules

### Trip Validity Rules
1. Trip must have non-null pickup and dropoff timestamps
2. Dropoff must be after pickup (duration > 0)
3. Total amount must equal sum of components (within $0.02 tolerance)
4. Trip distance must be ≥ 0
5. Passenger count must be 1-6 (regulatory limit)

### Revenue Calculation Rules
1. Total Amount = Fare + Extra + MTA Tax + Tip + Tolls + Improvement Surcharge + Congestion Surcharge
2. Cash payments have tip_amount = $0.00 (not tracked)
3. Voided trips excluded from revenue metrics
4. Disputed trips excluded until resolved

### Data Quality Rules
1. Missing or invalid values flagged in `dq_status` column
2. Records failing CRITICAL rules rejected (not in Gold layer)
3. Records failing HIGH rules quarantined for review
4. Records failing MEDIUM rules flagged but included

---

## Glossary Governance

**Owner:** Jennifer Park (Head of BI)  
**Review Frequency:** Quarterly  
**Update Process:** Submit change requests to BI team  
**Approval:** Business stakeholder + BI lead  

**Last Review:** 2026-02-05  
**Next Review:** 2026-05-01

---

## Related Documentation

- [Data Dictionary](data-dictionary.md) - Technical field reference
- [Model Diagram](model-diagram.md) - Star schema visualization
- [KPIs Document](../../Docs/strategy/kpis.md) - Detailed KPI definitions
- [Problem Statement](../../Docs/strategy/problem-statement.md) - Business context

---

**Version:** 1.0  
**Created:** 2026-02-05  
**Author:** Bianca (BiSemantic)
