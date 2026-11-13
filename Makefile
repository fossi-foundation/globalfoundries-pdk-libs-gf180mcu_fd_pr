# Copyright 2022 GlobalFoundries PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The top directory where environment will be created.
TOP_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

################################################################################
## Code linting
################################################################################
lint-python:
	uv run flake8
.PHONY: lint-python

################################################################################
## ngspice Regression section
################################################################################
# ngspice models regression
test-ngspice-%:
	cd models/ngspice/testing/regression/$*/ && python3 models_regression.py

################################################################################
## PCells Regression section
################################################################################
# fet main testing
test-nfet_03v3-pcells:
	cd cells/klayout/pymacros/testing/ && make test-nfet_03v3

test-nfet_05v0-pcells:
	cd cells/klayout/pymacros/testing/ && make test-nfet_05v0

test-nfet_06v0-pcells:
	cd cells/klayout/pymacros/testing/ && make test-nfet_06v0

test-pfet_03v3-pcells:
	cd cells/klayout/pymacros/testing/ && make test-pfet_03v3

test-pfet_05v0-pcells:
	cd cells/klayout/pymacros/testing/ && make test-pfet_05v0

test-pfet_06v0-pcells:
	cd cells/klayout/pymacros/testing/ && make test-pfet_06v0

# diode main testing
test-diode-pcells:
	cd cells/klayout/pymacros/testing/ && make test-diode

# moscap main testing
test-moscap-pcells:
	cd cells/klayout/pymacros/testing/ && make test-cap_mos

# mimcap main testing
test-mimcap-pcells:
	cd cells/klayout/pymacros/testing/ &&  make test-MIM

# res main testing
test-res-pcells:
	cd cells/klayout/pymacros/testing/ && make test-RES 

