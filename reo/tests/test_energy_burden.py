# *********************************************************************************
# REopt, Copyright (c) 2019-2020, Alliance for Sustainable Energy, LLC.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
#
# Neither the name of the copyright holder nor the names of its contributors may be
# used to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# *********************************************************************************

import json
import os
import copy
from tastypie.test import ResourceTestCaseMixin
from unittest import TestCase  # have to use unittest.TestCase to get tests to store to database, django.test.TestCase flushes db
from reo.models import ModelManager
from reo.utilities import check_common_outputs
from reo.nested_to_flat_output import nested_to_flat
import numpy as np
import pandas as pd

class EnergyBurdenTest(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(EnergyBurdenTest, self).setUp()
        #self.reopt_base = '/v1/job/'
        self.submit_url = '/v1/job/'
        self.results_url = '/v1/job/<run_uuid>/results/'
        self.post = {
            "Scenario": {
            "timeout_seconds": 420,
            "optimality_tolerance_techs": 0.7,
                "Site": {
                    "latitude": 37.78, "longitude": -122.45,

                    "annual_income_dollars": 20000,
                    "desired_energy_burden_threshold_percent": 0.06,

                    "Financial": {
                        "om_cost_escalation_pct": 0.01,
                        "escalation_pct": 0.006,
                        "offtaker_discount_pct": 0.07,
                        "analysis_years": 25,
                        "offtaker_tax_pct": 0.0
                    },
                    "LoadProfile": {
                        "doe_reference_name": "Hospital",
                    },
                    "LoadProfileBoilerFuel": {
                        "doe_reference_name": "LargeOffice",
                    },
                    "ElectricTariff": {
                        "urdb_label": '5cef0a415457a33576f60fe2',
                        #"eia": '14328', # May not be setup to take this input
                        #"urdb_rate_name": "E-19 Medium General Demand TOU",
                        #"blended_monthly_rates_us_dollars_per_kwh": [0.09] * 12,
                        #"blended_monthly_demand_charges_us_dollars_per_kw": [22] * 12,
                        "net_metering_limit_kw": 1e6,
                        "wholesale_rate_us_dollars_per_kwh": 0
                    },
                    "FuelTariff": {
                        "existing_boiler_fuel_type": "natural_gas",
                        "boiler_fuel_blended_monthly_rates_us_dollars_per_mmbtu": [11.0]*12,
                        "chp_fuel_type": "natural_gas",
                        "chp_fuel_blended_monthly_rates_us_dollars_per_mmbtu": [11.0]*12
                    },
                    "Storage": {
                        "max_kwh": 0,
                        "max_kw": 0,
                        "installed_cost_us_dollars_per_kw": 1000,
                        "installed_cost_us_dollars_per_kwh": 500,
                        "replace_cost_us_dollars_per_kw": 460,
                        "replace_cost_us_dollars_per_kwh": 230,
                        "macrs_option_years": 0,
                    },
                    "LoadProfileChillerThermal": {
                        "doe_reference_name": "LargeOffice",
                    },
                    "ElectricChiller": {
                    },
                    "Boiler": {
                        "boiler_efficiency": 0.8,
                        "existing_boiler_production_type_steam_or_hw": "steam",
                    },
                    "ColdTES": {
                        "min_gal": 0,
                        "max_gal": 0,
                        "installed_cost_us_dollars_per_gal": 3,
                        "thermal_decay_rate_fraction": 0.004,
                        "om_cost_us_dollars_per_gal": 0,
                        "internal_efficiency_pct": 0.97,
                    },
                    "HotTES": {
                        "min_gal": 0,
                        "max_gal": 0,
                        "installed_cost_us_dollars_per_gal": 3,
                        "thermal_decay_rate_fraction": 0.004,
                        "om_cost_us_dollars_per_gal": 0,
                        "internal_efficiency_pct": 0.97,
                    }
                }
            }
        }

    def get_response(self, data):
        initial_post = self.api_client.post(self.submit_url, format='json', data=data)
        postjsoncontent = json.loads(initial_post.content)
        try:
            uuid = postjsoncontent['run_uuid']
        except Exception as e:
            error_msg = postjsoncontent['messages']['error']
            print("test_energy_burden API error message: {}".format(error_msg))
            raise e
        response = json.loads(self.api_client.get(self.results_url.replace('<run_uuid>', str(uuid))).content)
        return response
        #return self.api_client.post(self.reopt_base, format='json', data=data)

    def test_energy_burden(self):    
        ## function to test if energy burden inputs translate to outputs properly

        ##expected outputs
        d_expected = dict()
        d_expected['year_one_energy_burden_percent'] = 1200/20000

        response = self.get_response(data=self.post)
        #self.assertHttpCreated(response)
        ## not fully clear for this code here

        ## calculated outputs