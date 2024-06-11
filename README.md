# Vision

This is a database of entities such as corporations (S-Corp, B-Corp, etc), limited liability companies, and their various stakeholders (other limited liability companies, venture capital-associated entities, private equity associated companies, etc).

@onefact has developed a power mapping exercise applied to the United States' health care system (https://www.figma.com/community/file/1357026523815963441/power-map-of-united-states-health-care-stakeholders-patients-providers-and-payors). 

In order to assess and verify whether this power mapping exercise has high fidelity or low fidelity to the state of affairs of network analysis and entity linkage in the United States health care and real estate sectors (and their inter-related capital flows and bids for liquidity), we need to use the @openc database.

## Methods

This repository relies on a mix of:

- large language models from @openai and @anthropics
- databases such as @duckdb (we are giving a talk about this work at duckcon in august: https://duckdb.org/2024/08/15/duckcon5.html)
- graph databases such as @kuzudb

## Financing 

This power mapping exercise is now supported by https://www.patientrightsadvocate.org/ through their grant of $100,000 to our organization, after our initial seed funding from @columbia and @SU-SWS.

## Conventions for collaboration

Please tackle any open issue and submit a pull request - we are working out conventions for collaboration in this manner.

Please submit an issue if you have a request for a feature, request for a visualization, or have any ideas on ways this data can be made more useful for health care, real estate use cases. 

If e-mail support is needed, please email us at [help@payless.health](mailto:help@payless.health).

### TODO 
- Create an "individuals view" which takes all individuals and puts in a single table with arrays of their associate linkages...
- Same for organizations

# Data Sources

### Ownership Data
https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/hospital-all-owners/api-docs
https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/home-health-agency-all-owners
