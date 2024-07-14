
# About
Does getting healthcare in the US feel like a labyrinth? Perhaps…
- You’re a patient, and you get a letter from some mysterious [“ACO” thingamajig](https://www.cms.gov/medicare/payment/fee-for-service-providers/shared-savings-program-ssp-acos/guidance-regulations#:~:text=An%20ACO%20or%20ACO%20participant,visit%20of%20the%20agreement%20period.), and now you’re not sure who they are and what they have to do with your doctor.
- You’re a retiring practitioner and you were approached by [Bartholomew Banks](https://www.youtube.com/watch?v=nG6ppzJwPYU) with an offer. You’re enticed, but worried what selling your practice might mean for patients and peers.
- Mom’s nursing home got acquired last week, and you’re wary of what it might mean.
- The insurer negotiated price of your medication is way higher than if you buy it without them involved...

While data on clinical professionals are heavily scrutinized, it’s harder to learn about the web of legal entities and business strategies operating behind the scenes.

At @onefact, we’re big believers that:
1. Incentives drive outcomes
2. Health policy is hard, and it’s not always clear which incentives are the best in any situation
3. In any case, you need transparency to find out

## Tools
This repository is meant to host **tools for understanding the labyrinth**. These will come in various forms, including:
- Open source graph databases which merge public CMS data with additional sources (Open Corporates, Price Transparency data, Payer / Provider websites, etc.)
- Websites and chat-based query interfaces that make the graph databases accessible to the general public.
- Research and experimental methods for surfacing relationships between entities involved in healthcare delivery which are not documented via structured data (sometimes purposefully obfuscated).

## Products
### PECOS Plus
Our first product is PECOS Plus, not to be confused with [PECOS 2.0](https://www.youtube.com/watch?v=P9ee_yWrsGU). PECOS Plus is an open source database which takes CMS PECOS enrollment and ownership data sources and maps them into a graph database. From there, we plan to...
- Create an interactive visual interface whereby people can explore relationships and propose opaque, or undocumented affiliate relationships.
- Integrate additional sources (Open Corporates, CMS Price Transparency data, etc.)
- Publish subgraphs curated by industry veterans that map the 800 lb gorillas, i.e. the largest payvidor entities (United Healthcare Group, CVS Health, Humana Inc.)
- Create a framework for experimenting with new methodologies to infer affiliate relationships. Similar to [CMS’ approach](https://data.cms.gov/resources/nursing-home-affiliated-entity-performance-measures-methodology) but with open source contributions.

If you have healthcare industry experience, sleuthing skills, or programming chops and want to help make this happen, please reach out please email us at [help@payless.health](mailto:help@payless.health).

## Financing 

This mapping exercise is now supported by https://www.patientrightsadvocate.org/ through their grant of $100,000 to our organization, after our initial seed funding from @columbia and @SU-SWS.

## Conventions for collaboration

Please tackle any open issue and submit a pull request - we are working out conventions for collaboration in this manner.

Feel free to submit an issue if you have a request for a feature, request for a visualization, or have any ideas on ways this data can be made more useful for health care use cases.
