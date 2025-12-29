"""
Ward-Level Policy Simulator for Delhi
Uses REAL ward data + evidence-based policy impacts from CPCB studies

This module enables ward councilors to simulate "what-if" scenarios:
- "What if I ban construction for 3 days?"
- "What if we implement odd-even?"
- "What combination of policies gives best ROI?"
"""

from datetime import datetime
from .delhi_ward_boundaries import (
    DELHI_WARDS_OFFICIAL,
    get_pollution_sources_for_ward,
    get_ward_by_id
)


# Real Delhi Policy Impacts (from CPCB studies)
DELHI_POLICY_IMPACTS = {
    "construction_ban": {
        "name": "Construction Ban",
        "description": "Halt all construction activities in the ward",
        "pm25_reduction_per_day": 0.06,  # 6% per day (CPCB 2019 study)
        "pm10_reduction_per_day": 0.08,  # 8% per day
        "cost_per_day_lakhs": 12,  # ₹12 lakh/day economic loss per ward
        "evidence": "CPCB Delhi Construction Ban Impact Study, Nov 2019",
        "confidence": 0.85,
        "targets": ["dust", "construction"],
        "implementation_time": "24 hours",
        "notes": "Most effective during Oct-Feb (peak construction season)"
    },
    
    "odd_even": {
        "name": "Odd-Even Vehicle Scheme",
        "description": "Alternate day vehicle restrictions based on plate numbers",
        "pm25_reduction": 0.04,  # 4% (Delhi 2016, 2019 trials)
        "pm10_reduction": 0.06,  # 6%
        "cost_lakhs": 50,  # ₹50 lakh enforcement per ward
        "evidence": "TERI Study on Delhi Odd-Even Impact, 2019",
        "confidence": 0.72,
        "targets": ["vehicular"],
        "implementation_time": "48 hours",
        "notes": "Limited impact due to exemptions (two-wheelers, women drivers, VIPs)"
    },
    
    "industrial_shutdown": {
        "name": "Industrial Capacity Reduction",
        "description": "Reduce industrial operations by specified percentage",
        "pm25_reduction_per_10pct": 0.015,  # 1.5% per 10% capacity reduction
        "cost_per_10pct_lakhs": 120,  # ₹1.2 crore per 10% reduction
        "evidence": "DPCC Industrial Emissions Study, 2021",
        "confidence": 0.78,
        "targets": ["industrial"],
        "implementation_time": "72 hours",
        "notes": "Affects Okhla, Bawana, Wazirabad industrial areas primarily"
    },
    
    "dust_control": {
        "name": "Water Sprinkling + Mechanical Sweeping",
        "description": "Regular road water sprinkling and mechanical sweeping",
        "pm25_reduction": 0.03,  # 3%
        "pm10_reduction": 0.08,  # 8% (more effective on coarse particles)
        "cost_per_km_per_day_lakhs": 0.003,  # ₹3,000 per km per day
        "evidence": "MCD Dust Control Effectiveness Report, 2022",
        "confidence": 0.80,
        "targets": ["dust"],
        "implementation_time": "12 hours",
        "notes": "Most effective on unpaved roads and construction zones"
    },
    
    "traffic_rerouting": {
        "name": "Heavy Vehicle Traffic Diversion",
        "description": "Divert heavy commercial vehicles away from ward",
        "pm25_reduction": 0.08,  # 8% on specific roads
        "localized": True,
        "cost_lakhs": 5,  # ₹5 lakh enforcement
        "evidence": "Delhi Traffic Police Study, 2020",
        "confidence": 0.70,
        "targets": ["vehicular"],
        "implementation_time": "24 hours",
        "notes": "Effective for transport hubs like Anand Vihar, Azadpur"
    },
    
    "green_barrier": {
        "name": "Temporary Green Barriers",
        "description": "Deploy portable green barriers and misting systems",
        "pm25_reduction": 0.02,  # 2% (localized)
        "timeline_days": 7,  # Takes time to show effect
        "cost_lakhs": 20,  # ₹20 lakh setup
        "evidence": "TERI Urban Forestry Study, 2021",
        "confidence": 0.65,
        "targets": ["dust", "vehicular"],
        "implementation_time": "7 days",
        "notes": "Long-term solution, immediate impact limited"
    },
    
    "smog_tower": {
        "name": "Deploy Smog Tower/Anti-Smog Gun",
        "description": "Deploy mobile anti-smog guns in high pollution areas",
        "pm25_reduction": 0.05,  # 5% in 500m radius
        "radius_meters": 500,
        "cost_per_unit_lakhs": 15,  # ₹15 lakh per unit
        "evidence": "IIT Delhi Smog Tower Study, 2021",
        "confidence": 0.60,
        "targets": ["dust", "vehicular"],
        "implementation_time": "6 hours",
        "notes": "Effective only in immediate vicinity, weather dependent"
    },
    
    "public_transport_boost": {
        "name": "Enhanced Public Transport",
        "description": "Increase bus frequency and metro feeder services",
        "pm25_reduction": 0.02,  # 2% (long-term behavioral change)
        "cost_lakhs": 100,  # ₹1 crore subsidy
        "evidence": "Delhi Transport Corporation Study, 2022",
        "confidence": 0.55,
        "targets": ["vehicular"],
        "implementation_time": "7 days",
        "notes": "Requires coordination with DTC and DMRC"
    }
}


class WardPolicySimulator:
    """
    Simulate policy impacts on specific Delhi wards using real data
    """
    
    @classmethod
    def get_available_policies(cls):
        """Return list of all available policies with details"""
        return {
            policy_id: {
                "name": policy["name"],
                "description": policy["description"],
                "confidence": f"{policy['confidence']*100:.0f}%",
                "evidence": policy["evidence"],
                "implementation_time": policy.get("implementation_time", "Varies"),
                "targets": policy["targets"]
            }
            for policy_id, policy in DELHI_POLICY_IMPACTS.items()
        }
    
    @classmethod
    def analyze_ward_pollution(cls, ward_id, current_pm25):
        """
        Analyze pollution sources for a specific ward
        
        Returns:
            - Breakdown by source
            - Top contributors
            - Recommended policies based on sources
        """
        ward = get_ward_by_id(ward_id)
        if not ward:
            return {"error": f"Ward {ward_id} not found"}
        
        # Get ward-specific pollution sources
        sources = get_pollution_sources_for_ward(ward_id)
        
        # Calculate absolute contributions
        source_breakdown = {}
        for source, percentage in sources.items():
            contribution_ug = current_pm25 * percentage
            source_breakdown[source] = {
                "percentage": round(percentage * 100, 1),
                "contribution_ug_m3": round(contribution_ug, 2)
            }
        
        # Sort by contribution
        top_sources = sorted(
            source_breakdown.items(),
            key=lambda x: x[1]["percentage"],
            reverse=True
        )
        
        # Recommend policies based on top sources
        recommended_policies = []
        for source, data in top_sources[:2]:  # Top 2 sources
            if source in ["construction", "dust"]:
                recommended_policies.extend(["construction_ban", "dust_control", "smog_tower"])
            elif source == "vehicular":
                recommended_policies.extend(["odd_even", "traffic_rerouting", "public_transport_boost"])
            elif source == "industrial":
                recommended_policies.append("industrial_shutdown")
        
        # Remove duplicates while preserving order
        recommended_policies = list(dict.fromkeys(recommended_policies))
        
        return {
            "ward_id": ward_id,
            "ward_name": ward["name"],
            "ward_type": ward["type"],
            "zone": ward["zone"],
            "current_pm25": current_pm25,
            "population": ward.get("population_2024_est", 0),
            "area_km2": ward.get("area_km2", 0),
            "source_breakdown": source_breakdown,
            "top_sources": [
                {
                    "source": src[0].replace("_", " ").title(),
                    "percentage": src[1]["percentage"],
                    "contribution_ug_m3": src[1]["contribution_ug_m3"]
                }
                for src in top_sources
            ],
            "recommended_policies": recommended_policies[:4],
            "is_hotspot": ward.get("pollution_hotspot", False)
        }
    
    @classmethod
    def simulate_policy(cls, ward_id, current_pm25, policy_type, policy_params):
        """
        Simulate a single policy impact
        
        Args:
            ward_id: Delhi ward ID (1-40)
            current_pm25: Current PM2.5 level in µg/m³
            policy_type: One of DELHI_POLICY_IMPACTS keys
            policy_params: Dict with policy-specific params
                - construction_ban: {"days": 3}
                - odd_even: {"enabled": True}
                - industrial_shutdown: {"capacity_reduction_pct": 50}
                - dust_control: {"road_km": 25}
                - traffic_rerouting: {"enabled": True}
                - smog_tower: {"units": 2}
        
        Returns:
            Detailed impact analysis with cost-benefit
        """
        ward = get_ward_by_id(ward_id)
        if not ward:
            return {"error": f"Ward {ward_id} not found"}
        
        policy_data = DELHI_POLICY_IMPACTS.get(policy_type)
        if not policy_data:
            return {"error": f"Invalid policy type: {policy_type}"}
        
        # Get ward pollution sources
        sources = get_pollution_sources_for_ward(ward_id)
        
        # Calculate policy effectiveness based on ward type and sources
        pm25_reduction_pct = 0
        cost_lakhs = 0
        affected_details = []
        
        if policy_type == "construction_ban":
            days = policy_params.get("days", 1)
            
            # Reduction depends on construction/dust contribution in this ward
            construction_contribution = sources.get("construction", 0) + sources.get("dust", 0) * 0.5
            
            # More effective in wards with higher construction activity
            effectiveness_multiplier = 1.0
            if ward["type"] in ["industrial", "dense_residential", "commercial"]:
                effectiveness_multiplier = 1.2
            
            pm25_reduction_pct = (
                policy_data["pm25_reduction_per_day"] * 
                days * 
                (construction_contribution / 0.3) *  # Normalize to 30% baseline
                effectiveness_multiplier
            )
            
            cost_lakhs = policy_data["cost_per_day_lakhs"] * days
            
            # Estimate affected sites based on ward area
            construction_sites = int(ward.get("area_km2", 3) * 2)  # ~2 sites per km²
            
            affected_details = [
                f"~{construction_sites} construction sites halted",
                f"Duration: {days} days",
                f"Economic impact: ₹{cost_lakhs:.1f} lakh"
            ]
        
        elif policy_type == "odd_even":
            if not policy_params.get("enabled"):
                return {"error": "Policy not enabled in params"}
            
            vehicular_contribution = sources.get("vehicular", 0)
            
            # More effective in commercial/transport areas
            effectiveness_multiplier = 1.0
            if ward["type"] in ["transport_hub", "commercial"]:
                effectiveness_multiplier = 1.3
            elif ward["type"] == "affluent_residential":
                effectiveness_multiplier = 1.2  # Higher car ownership
            
            pm25_reduction_pct = (
                policy_data["pm25_reduction"] * 
                (vehicular_contribution / 0.4) *  # Normalize to 40% baseline
                effectiveness_multiplier
            )
            
            cost_lakhs = policy_data["cost_lakhs"]
            
            # Estimate vehicles affected
            vehicles_per_1000 = 150  # Delhi average
            total_vehicles = int(ward.get("population_2024_est", 50000) * vehicles_per_1000 / 1000)
            affected_vehicles = int(total_vehicles * 0.5)
            
            affected_details = [
                f"~{affected_vehicles:,} vehicles affected daily",
                f"Major roads: {', '.join(ward.get('major_roads', ['Various'])[:2])}",
                f"Enforcement cost: ₹{cost_lakhs:.1f} lakh"
            ]
        
        elif policy_type == "industrial_shutdown":
            capacity_reduction = policy_params.get("capacity_reduction_pct", 0)
            
            if capacity_reduction > 100 or capacity_reduction < 0:
                return {"error": "capacity_reduction_pct must be 0-100"}
            
            industrial_contribution = sources.get("industrial", 0)
            
            # Only effective in industrial wards
            if industrial_contribution < 0.1:
                return {
                    "ward_id": ward_id,
                    "ward_name": ward["name"],
                    "error": "This ward has minimal industrial activity (<10%)",
                    "industrial_contribution": f"{industrial_contribution*100:.1f}%",
                    "recommendation": "Consider other policies like dust_control or traffic_rerouting"
                }
            
            pm25_reduction_pct = (
                policy_data["pm25_reduction_per_10pct"] * 
                (capacity_reduction / 10) * 
                (industrial_contribution / 0.35)  # Normalize to 35% baseline
            )
            
            cost_lakhs = policy_data["cost_per_10pct_lakhs"] * (capacity_reduction / 10)
            
            industrial_areas = ward.get("industrial_areas", [])
            affected_details = [
                f"{len(industrial_areas)} industrial areas affected",
                f"Capacity reduced by {capacity_reduction}%",
                f"Areas: {', '.join(industrial_areas[:2]) if industrial_areas else 'General industrial'}",
                f"Economic impact: ₹{cost_lakhs/100:.2f} crore"
            ]
        
        elif policy_type == "dust_control":
            road_km = policy_params.get("road_km", 0)
            
            if road_km <= 0:
                road_km = ward.get("area_km2", 3) * 3  # Default: 3km per km² area
            
            dust_contribution = sources.get("dust", 0)
            
            pm25_reduction_pct = policy_data["pm25_reduction"] * (dust_contribution / 0.25)
            cost_lakhs = policy_data["cost_per_km_per_day_lakhs"] * road_km * 7  # 7 days
            
            affected_details = [
                f"{road_km:.1f} km of roads covered",
                "Water sprinkling: 3 times daily",
                "Mechanical sweeping: Twice daily",
                f"Weekly cost: ₹{cost_lakhs:.2f} lakh"
            ]
        
        elif policy_type == "traffic_rerouting":
            if not policy_params.get("enabled"):
                return {"error": "Policy not enabled in params"}
            
            vehicular_contribution = sources.get("vehicular", 0)
            
            # Most effective in transport hubs
            effectiveness_multiplier = 1.0
            if ward["type"] == "transport_hub":
                effectiveness_multiplier = 1.5
            elif "NH" in str(ward.get("major_roads", [])) or "Ring Road" in str(ward.get("major_roads", [])):
                effectiveness_multiplier = 1.3
            
            pm25_reduction_pct = (
                policy_data["pm25_reduction"] * 
                (vehicular_contribution / 0.4) * 
                effectiveness_multiplier
            )
            
            cost_lakhs = policy_data["cost_lakhs"]
            
            affected_details = [
                "Heavy commercial vehicles diverted",
                f"Target corridors: {', '.join(ward.get('major_roads', ['Main roads'])[:2])}",
                "24-hour enforcement",
                f"Enforcement cost: ₹{cost_lakhs:.1f} lakh"
            ]
        
        elif policy_type == "smog_tower":
            units = policy_params.get("units", 1)
            
            # Each unit covers ~500m radius
            coverage_km2 = units * 0.785  # π * (0.5)²
            ward_coverage = min(coverage_km2 / ward.get("area_km2", 3), 1.0)
            
            pm25_reduction_pct = policy_data["pm25_reduction"] * ward_coverage
            cost_lakhs = policy_data["cost_per_unit_lakhs"] * units
            
            affected_details = [
                f"{units} anti-smog gun(s) deployed",
                f"Coverage: {ward_coverage*100:.0f}% of ward area",
                f"Effective radius: {units * 500}m total",
                f"Setup cost: ₹{cost_lakhs:.1f} lakh"
            ]
        
        elif policy_type == "green_barrier":
            pm25_reduction_pct = policy_data["pm25_reduction"]
            cost_lakhs = policy_data["cost_lakhs"]
            
            affected_details = [
                "Portable green barriers installed",
                "Misting systems activated",
                f"Timeline: {policy_data['timeline_days']} days for full effect",
                f"Setup cost: ₹{cost_lakhs:.1f} lakh"
            ]
        
        elif policy_type == "public_transport_boost":
            vehicular_contribution = sources.get("vehicular", 0)
            
            pm25_reduction_pct = policy_data["pm25_reduction"] * (vehicular_contribution / 0.4)
            cost_lakhs = policy_data["cost_lakhs"]
            
            metro_stations = ward.get("metro_stations", [])
            affected_details = [
                f"Bus frequency increased by 50%",
                f"Metro feeder services: {len(metro_stations)} stations",
                "Free/subsidized rides during peak hours",
                f"Subsidy cost: ₹{cost_lakhs/100:.1f} crore"
            ]
        
        # Cap reduction at reasonable maximum
        pm25_reduction_pct = min(pm25_reduction_pct, 0.25)  # Max 25% from single policy
        
        # Calculate predicted PM2.5
        predicted_pm25 = current_pm25 * (1 - pm25_reduction_pct)
        absolute_reduction = current_pm25 - predicted_pm25
        
        # Calculate health benefits
        health_benefits = cls._calculate_health_benefits(
            ward.get("population_2024_est", 50000),
            absolute_reduction,
            cost_lakhs
        )
        
        # Generate recommendation
        recommendation = cls._generate_recommendation(
            pm25_reduction_pct,
            cost_lakhs,
            ward.get("population_2024_est", 50000),
            policy_data["confidence"]
        )
        
        return {
            "ward_id": ward_id,
            "ward_name": ward["name"],
            "ward_type": ward["type"],
            
            "policy": {
                "id": policy_type,
                "name": policy_data["name"],
                "description": policy_data["description"],
                "parameters": policy_params
            },
            
            "current_conditions": {
                "pm25": round(current_pm25, 1),
                "population": ward.get("population_2024_est", 0),
                "area_km2": ward.get("area_km2", 0)
            },
            
            "predicted_impact": {
                "pm25_before": round(current_pm25, 1),
                "pm25_after": round(predicted_pm25, 1),
                "reduction_ug_m3": round(absolute_reduction, 1),
                "reduction_percent": round(pm25_reduction_pct * 100, 1),
                "timeline": policy_data.get("implementation_time", "48-72 hours")
            },
            
            "cost_analysis": {
                "total_cost_lakhs": round(cost_lakhs, 2),
                "total_cost_crore": round(cost_lakhs / 100, 3),
                "cost_per_ug_reduced": round(cost_lakhs / absolute_reduction, 2) if absolute_reduction > 0 else 0,
                "affected": affected_details
            },
            
            "health_benefits": health_benefits,
            
            "evidence": {
                "source": policy_data["evidence"],
                "confidence": f"{policy_data['confidence']*100:.0f}%",
                "notes": policy_data.get("notes", "")
            },
            
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat()
        }
    
    @classmethod
    def simulate_multiple_policies(cls, ward_id, current_pm25, policies):
        """
        Simulate combination of multiple policies
        
        Args:
            ward_id: Ward ID
            current_pm25: Current PM2.5
            policies: List of dicts like:
                [
                    {"type": "construction_ban", "params": {"days": 3}},
                    {"type": "odd_even", "params": {"enabled": True}}
                ]
        """
        ward = get_ward_by_id(ward_id)
        if not ward:
            return {"error": f"Ward {ward_id} not found"}
        
        results = []
        cumulative_reduction = 0
        total_cost_lakhs = 0
        
        for policy in policies:
            result = cls.simulate_policy(
                ward_id,
                current_pm25,
                policy["type"],
                policy.get("params", {})
            )
            
            if "error" not in result:
                results.append(result)
                cumulative_reduction += result["predicted_impact"]["reduction_percent"]
                total_cost_lakhs += result["cost_analysis"]["total_cost_lakhs"]
        
        # Apply diminishing returns for combined policies
        # Each additional policy is ~90% as effective
        effective_reduction = 0
        remaining = 100
        for i, result in enumerate(results):
            policy_reduction = result["predicted_impact"]["reduction_percent"]
            effective_policy_reduction = policy_reduction * (0.9 ** i)
            effective_reduction += (remaining * effective_policy_reduction / 100)
            remaining -= effective_policy_reduction
        
        combined_pm25 = current_pm25 * (1 - effective_reduction / 100)
        
        # Calculate combined health benefits
        combined_health = cls._calculate_health_benefits(
            ward.get("population_2024_est", 50000),
            current_pm25 - combined_pm25,
            total_cost_lakhs
        )
        
        return {
            "ward_id": ward_id,
            "ward_name": ward["name"],
            "policies_applied": len(results),
            
            "individual_results": [
                {
                    "policy": r["policy"]["name"],
                    "reduction_percent": r["predicted_impact"]["reduction_percent"],
                    "cost_lakhs": r["cost_analysis"]["total_cost_lakhs"]
                }
                for r in results
            ],
            
            "combined_impact": {
                "current_pm25": round(current_pm25, 1),
                "predicted_pm25": round(combined_pm25, 1),
                "total_reduction_ug_m3": round(current_pm25 - combined_pm25, 1),
                "total_reduction_percent": round(effective_reduction, 1),
                "simple_sum_percent": round(cumulative_reduction, 1),
                "diminishing_returns_note": "Combined effect is less than sum due to overlapping impacts"
            },
            
            "cost_summary": {
                "total_cost_lakhs": round(total_cost_lakhs, 2),
                "total_cost_crore": round(total_cost_lakhs / 100, 3),
                "cost_per_percent_reduction": round(total_cost_lakhs / effective_reduction, 2) if effective_reduction > 0 else 0
            },
            
            "health_benefits": combined_health,
            
            "recommendation": cls._generate_combined_recommendation(
                effective_reduction,
                total_cost_lakhs,
                ward.get("population_2024_est", 50000),
                len(results)
            ),
            
            "timestamp": datetime.now().isoformat()
        }
    
    @classmethod
    def get_ai_recommendation(cls, ward_id, current_pm25, budget_lakhs=None):
        """
        AI-powered policy recommendation for a ward
        
        Analyzes pollution sources and recommends optimal policy mix
        """
        ward = get_ward_by_id(ward_id)
        if not ward:
            return {"error": f"Ward {ward_id} not found"}
        
        sources = get_pollution_sources_for_ward(ward_id)
        
        # Sort sources by contribution
        top_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)
        
        recommended_policies = []
        reasoning = []
        
        # Determine severity
        if current_pm25 > 300:
            severity = "EMERGENCY"
            reasoning.append(f"🚨 EMERGENCY: PM2.5 at {current_pm25} µg/m³ (20x WHO limit)")
        elif current_pm25 > 200:
            severity = "SEVERE"
            reasoning.append(f"⚠️ SEVERE pollution: PM2.5 at {current_pm25} µg/m³")
        elif current_pm25 > 100:
            severity = "VERY_POOR"
            reasoning.append(f"⚠️ Very Poor air quality: PM2.5 at {current_pm25} µg/m³")
        else:
            severity = "POOR"
            reasoning.append(f"Moderate-Poor air quality: PM2.5 at {current_pm25} µg/m³")
        
        # Build policy recommendations based on sources and severity
        if severity in ["EMERGENCY", "SEVERE"]:
            # Aggressive multi-pronged approach
            if top_sources[0][0] in ["construction", "dust"]:
                recommended_policies.append({
                    "type": "construction_ban",
                    "params": {"days": 5 if severity == "EMERGENCY" else 3},
                    "priority": "CRITICAL"
                })
                reasoning.append(f"🏗️ Construction/dust is {top_sources[0][1]*100:.0f}% - ban recommended")
            
            if sources.get("vehicular", 0) > 0.25:
                recommended_policies.append({
                    "type": "traffic_rerouting",
                    "params": {"enabled": True},
                    "priority": "HIGH"
                })
                reasoning.append(f"🚛 Heavy vehicle diversion for {sources.get('vehicular', 0)*100:.0f}% vehicular pollution")
            
            # Always add smog guns in emergency
            recommended_policies.append({
                "type": "smog_tower",
                "params": {"units": 3 if severity == "EMERGENCY" else 2},
                "priority": "HIGH"
            })
            reasoning.append("💨 Deploy anti-smog guns for immediate relief")
            
            # Dust control
            recommended_policies.append({
                "type": "dust_control",
                "params": {"road_km": ward.get("area_km2", 3) * 4},
                "priority": "HIGH"
            })
            reasoning.append("🚿 Intensive water sprinkling on all major roads")
        
        elif severity == "VERY_POOR":
            # Targeted approach based on top source
            if top_sources[0][0] in ["construction", "dust"]:
                recommended_policies.append({
                    "type": "construction_ban",
                    "params": {"days": 2},
                    "priority": "HIGH"
                })
                recommended_policies.append({
                    "type": "dust_control",
                    "params": {"road_km": ward.get("area_km2", 3) * 3},
                    "priority": "MEDIUM"
                })
                reasoning.append(f"Target dust sources ({top_sources[0][1]*100:.0f}% contribution)")
            
            elif top_sources[0][0] == "vehicular":
                recommended_policies.append({
                    "type": "traffic_rerouting",
                    "params": {"enabled": True},
                    "priority": "HIGH"
                })
                recommended_policies.append({
                    "type": "odd_even",
                    "params": {"enabled": True},
                    "priority": "MEDIUM"
                })
                reasoning.append(f"Target vehicular emissions ({top_sources[0][1]*100:.0f}% contribution)")
            
            elif top_sources[0][0] == "industrial":
                recommended_policies.append({
                    "type": "industrial_shutdown",
                    "params": {"capacity_reduction_pct": 30},
                    "priority": "HIGH"
                })
                reasoning.append(f"Target industrial emissions ({top_sources[0][1]*100:.0f}% contribution)")
        
        else:  # POOR
            # Preventive measures
            recommended_policies.append({
                "type": "dust_control",
                "params": {"road_km": ward.get("area_km2", 3) * 2},
                "priority": "MEDIUM"
            })
            reasoning.append("💨 Preventive dust control measures")
            
            if ward["type"] == "transport_hub":
                recommended_policies.append({
                    "type": "traffic_rerouting",
                    "params": {"enabled": True},
                    "priority": "MEDIUM"
                })
                reasoning.append("🚛 Divert heavy vehicles from transport hub")
        
        # Apply budget constraint if provided
        if budget_lakhs:
            reasoning.append(f"💰 Budget constraint: ₹{budget_lakhs} lakh")
            # Filter policies by budget (simplified)
            filtered_policies = []
            remaining_budget = budget_lakhs
            
            for policy in recommended_policies:
                # Estimate cost
                estimated_cost = cls._estimate_policy_cost(policy, ward)
                if estimated_cost <= remaining_budget:
                    filtered_policies.append(policy)
                    remaining_budget -= estimated_cost
            
            recommended_policies = filtered_policies
            reasoning.append(f"Filtered to {len(recommended_policies)} policies within budget")
        
        # Run simulation
        simulation = cls.simulate_multiple_policies(
            ward_id,
            current_pm25,
            recommended_policies
        )
        
        return {
            "ward_id": ward_id,
            "ward_name": ward["name"],
            "ward_type": ward["type"],
            
            "current_situation": {
                "pm25": current_pm25,
                "severity": severity,
                "population_affected": ward.get("population_2024_est", 0),
                "top_pollution_sources": [
                    {"source": src[0].replace("_", " ").title(), "contribution": f"{src[1]*100:.1f}%"}
                    for src in top_sources[:3]
                ]
            },
            
            "ai_recommendation": {
                "recommended_policies": recommended_policies,
                "reasoning": reasoning,
                "expected_outcome": simulation.get("combined_impact", {}),
                "total_cost": simulation.get("cost_summary", {}),
                "health_benefits": simulation.get("health_benefits", {})
            },
            
            "simulation_details": simulation,
            "timestamp": datetime.now().isoformat()
        }
    
    @classmethod
    def _estimate_policy_cost(cls, policy, ward):
        """Quick cost estimation for budget filtering"""
        policy_type = policy["type"]
        params = policy.get("params", {})
        policy_data = DELHI_POLICY_IMPACTS.get(policy_type, {})
        
        if policy_type == "construction_ban":
            return policy_data.get("cost_per_day_lakhs", 12) * params.get("days", 1)
        elif policy_type == "industrial_shutdown":
            return policy_data.get("cost_per_10pct_lakhs", 120) * (params.get("capacity_reduction_pct", 30) / 10)
        elif policy_type == "dust_control":
            return policy_data.get("cost_per_km_per_day_lakhs", 0.003) * params.get("road_km", 10) * 7
        elif policy_type == "smog_tower":
            return policy_data.get("cost_per_unit_lakhs", 15) * params.get("units", 1)
        else:
            return policy_data.get("cost_lakhs", 50)
    
    @classmethod
    def _calculate_health_benefits(cls, population, pm25_reduction, cost_lakhs):
        """Calculate health benefit economics using WHO methodology"""
        if pm25_reduction <= 0:
            return {
                "lives_benefited": 0,
                "healthcare_savings_lakhs": 0,
                "net_benefit_lakhs": 0,
                "verdict": "NO_IMPACT"
            }
        
        # WHO: 10 µg/m³ reduction = ~6% reduction in mortality risk
        mortality_risk_reduction = (pm25_reduction / 10) * 0.06
        
        # Respiratory illness reduction estimate
        respiratory_reduction = (pm25_reduction / 10) * 0.10
        
        # Healthcare cost savings
        # Average healthcare cost per respiratory case: ₹15,000
        # Respiratory cases per 1000 people at high pollution: ~50
        respiratory_cases_avoided = population * 0.05 * respiratory_reduction
        healthcare_savings = respiratory_cases_avoided * 15000 / 100000  # In lakhs
        
        # Calculate lives statistically saved
        # Delhi crude death rate: ~5 per 1000
        annual_deaths = population * 0.005
        lives_saved_annually = annual_deaths * mortality_risk_reduction
        
        # Net benefit
        net_benefit = healthcare_savings - cost_lakhs
        roi = ((healthcare_savings - cost_lakhs) / cost_lakhs * 100) if cost_lakhs > 0 else 0
        
        return {
            "population_benefited": population,
            "pm25_reduction": round(pm25_reduction, 1),
            "mortality_risk_reduction": f"{mortality_risk_reduction*100:.2f}%",
            "respiratory_cases_avoided": int(respiratory_cases_avoided),
            "statistical_lives_saved": round(lives_saved_annually, 2),
            "healthcare_savings_lakhs": round(healthcare_savings, 2),
            "policy_cost_lakhs": round(cost_lakhs, 2),
            "net_benefit_lakhs": round(net_benefit, 2),
            "roi_percent": round(roi, 1),
            "cost_per_life_saved_lakhs": round(cost_lakhs / lives_saved_annually, 2) if lives_saved_annually > 0 else "N/A",
            "verdict": "COST_EFFECTIVE" if roi > 0 else "COSTLY_BUT_NECESSARY" if pm25_reduction > 30 else "REVIEW_ALTERNATIVES"
        }
    
    @classmethod
    def _generate_recommendation(cls, pm25_reduction_pct, cost_lakhs, population, confidence):
        """Generate recommendation verdict for single policy"""
        cost_per_person = (cost_lakhs * 100000) / population if population > 0 else float('inf')
        
        if pm25_reduction_pct > 0.15 and cost_per_person < 100 and confidence > 0.75:
            return {
                "verdict": "HIGHLY_RECOMMENDED",
                "emoji": "✅",
                "reason": "High impact, cost-effective, strong evidence base"
            }
        elif pm25_reduction_pct > 0.10 and confidence > 0.70:
            return {
                "verdict": "RECOMMENDED",
                "emoji": "✅",
                "reason": "Good impact with reasonable cost and evidence"
            }
        elif pm25_reduction_pct > 0.05:
            return {
                "verdict": "CONSIDER",
                "emoji": "⚠️",
                "reason": "Moderate impact - consider alongside other policies"
            }
        else:
            return {
                "verdict": "LOW_PRIORITY",
                "emoji": "❌",
                "reason": "Limited impact for this ward type - explore alternatives"
            }
    
    @classmethod
    def _generate_combined_recommendation(cls, total_reduction, total_cost, population, num_policies):
        """Generate recommendation for combined policies"""
        cost_per_percent = total_cost / total_reduction if total_reduction > 0 else float('inf')
        
        if total_reduction > 20 and cost_per_percent < 10:
            verdict = "EXCELLENT_STRATEGY"
            emoji = "🌟"
            reason = f"{total_reduction:.1f}% reduction achievable - implement immediately"
        elif total_reduction > 15:
            verdict = "GOOD_STRATEGY"
            emoji = "✅"
            reason = f"Solid {total_reduction:.1f}% reduction expected"
        elif total_reduction > 10:
            verdict = "MODERATE_STRATEGY"
            emoji = "⚠️"
            reason = f"{total_reduction:.1f}% reduction - consider adding more policies"
        else:
            verdict = "NEEDS_REVIEW"
            emoji = "🔄"
            reason = "Limited combined impact - review policy selection"
        
        return {
            "verdict": verdict,
            "emoji": emoji,
            "reason": reason,
            "policies_count": num_policies,
            "efficiency": f"₹{cost_per_percent:.1f} lakh per 1% reduction"
        }
