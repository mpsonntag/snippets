# RDM Strategy of NFDI Neuroscience (Thomas Wachtler)

- Neuroscience data are diverse and complex
- sharing of data is hard due to this diversity
- new concepts of data management need to be developed and introduced to make data sharable and usable in the future.

## NFDI Neuroscience - Concept and approach
- coordinate interaction of expert neuroscientists to address RDM needs and function as nodes for solution development.

## RDM Strategy
- there already are many neuroscience resources out there
- what needs to be done is to make them aware of each other and make them interoperable
- also an infrastructure is needed to create common workflows with and for these tools.
- participation of labs is required!

## How to participate
- NFDI should be a platform to collect tools from labs and make them available and support in further development.

## Comments
- Phillip Tovote
  - the community approach is very appreciated
  - sections (task areas) are a good idea
  - how can the community motivate itself for the task at hand. the system is still mainly driven by the impact factor and there is no reward for proper RDM and sharing might be even contra productive for a PhDs or a postdocs career.
  - this is a complex, philosphical discussion but should be held.
  - alternative incentives should be implemented into the initiative giving an outlook in how proper RDM can help with the career.
- Thomas Wachtler:
  - scientists are more effective with proper RDM. By starting a community it will be easier to overcome the immediate reward barrier.
  - with respect to open data there is no established credit system yet, but journals already support data publications and credits for data publication will come in time.
- Otto Witte
  - many data repositories are too much work and too much documentation is required.
  - more positive impulses for data publications are required
  - funded research must demand open data publication
- Lucia Melloni
  - use this initiative to develop guidelines which can work as an incentive for a community.
  - they are working in a large collaboration and RDM is an issue; the data sharing is difficult and the rewards for limited positions like PhDs are not available; they need to profit in some way.
  - the rewards need to be actively developed
- Sonja Gruen:
  - first round of student will have a hard time
  - second round of students can work on the collected data already
    - we need to overcome this initial collection step
- Michael Hanke
    - there is a point in additional incentives
    - but the initiative should remove the need for incentives and make the RDM so easy to make training less costly
- Karl Kafitz
    - students actually like RDM if they get the chance
    - a problem are the universities since they do not give much support with respect to RDM in individual labs - there money is a problem, as soon as money is involved, the universities get hesitant.
- Michael Denker
    - students are extremely motivated
    - are lacking the experience in RDM topics themselves since they come from different background
    - funding and acknowledging RDM efforts are important
- Julien Colomb
    - the DFG should be actively engaged in requiring incentives for grants with respect to RDM

# Common Infrastructure (Michael Hanke, Thomas Wachtler)

- each slide has a link to a feedback document
- use it for later collection of ideas and discussion

- NFDI will not provide hardware
- NFDI will not provide a single solution for all of neuroscience

- there already is infrastructure available in many institutes
- problem is the connection between the infrastructures

## Aims for NFDI
- NFDI should solve this connection problem
  - introduce a common data structure
  - introduce a common interface between existing repositories
  - collect metadata
  - continuously test existing software and storage to keep it a trustworthy environment

## Datalad principles
- datalad could be the common interface between existing repos

interoparable with many services
- gin
- cbrain
- etc

## Access 3rd party data: preserved stewardship
e.g. UKBiobank

## what are we aiming for
- issue in human neuroscience - data protection
  - develop a data structure that in itself can be called anonymous - no hashes etc - but is capable of tracking datasets
  - provide only the data required for computation
  - can provide a basis for large scale dataset analysis which is currently hard to do
- prototype to extract metadata automatically from data sets and introduce them to google - google for data sets
- have workshops where scientists ask a scientific question and solve it while on the side learn how to do RDM

## Comments

- Julien Colomb
  - using DataLad with GIN. DataLad is too computer scientific; how to make access easier for biologists -> MHanke: GUI is not a solution, automatically extracting metadata should already help; interfaces for metadata should be developed as well to make required metadata entry low key as well. community needs to be engaged for tailored solutions to this end. NFDI Neuro should be the platform for it. Convenience and robustness need to be balanced.
- Stephan Hachinger, LRZ Graching
  - interested in contributing to RDM; some efforts for writing adaptors to export metadata to search engines. offer capacity to write adaptors for NFDI projects as well. Also offer in terms of infrastructure itself.
  - is the NFDI planning to deploy datalad on computing centers; how to best interact with NFDI in the next weeks; MHanke: will not go to every institute and deploy services but will establish collaborations with institutes - transfer teams are permanently reachable people from domains available for the institutes.
- Timo Dickscheid:
  - follow up in Julien; gap between developers and analysts and labmates - within the lab there are individual solutions.
  - datalad makes sense and would like to use it but was too difficult for neuroanatomists.
  - agrees that a custom interface for user groups would make much sense, they are doing this right now to put a mask on top of datalad and it works quite well.
  - the NFDI should also be a point of access to share these user interfaces.
  - MHanke: agreed, also the collaboration aspect in development is the proper approach; a common layer for collaborative development needs to be established via the NFDI and made known to the experts in the lab so they can participate and benefit.
- Lucia Melloni
    - have problem in documenting complete metadata, to make them searchable. community standards in metadata are required.
    - MHanke: Datalad is dumb in the sense that it does not get in the way. Start with low quality metadata standards and grow up from there to reduce the barrier. the researcher has to be rewarded somehow for entering high quality metadata. Datalad already provides a local search enginge for entered metadata w/o the need for a database.
- Tamas Spisak (UKE Essen)
  - uses datalad; plan to use datalad for imaging data; how is the stance with respect to GDPR
  - is there direct support in datalad 
  - MHanke: virtual brain cloud - assessment of GDPR compliance of datasets; datalad cannot give GDPR compliance out of the box
- Philip Tovote:
  - marketplace is a very good idea
  - would NFDI Neuro provide a platform for this kind of self organized marketplace?
  - MHanke: the answer has to be yes. NFDI Neuro should be the coordinating entity and has to provide this kind of service. But: the groups have to be defined first and then the groups can talk about metadata. start small and succeed and not aim high and delay.
- Julien Coulomb
  - NFDI Neuro infrastructure and Datalad: is this the only content or will there be other tools
  - MHanke: infrastructure is a wide field and not just datalad. the core purpose is to connect tools. It is not about consolidation into a single tool. It should be and stay independently extensible and should stay as decentral as possible. If a new tool emerges that is better capable of getting the job done, it should be used and be easy to switch.
  - TWachtler: as clarification: infrastructure is used in a general sense and not in the sense of specific tools.

## Chat
Michael Hanke
- https://tinyurl.com/nfdi-ta0 

Julien Colomb
should the neuro NFDI also work in a way to share these UI in the community, it is always easier to tweak an existing system than starting from scratch ?

Thomas Wachtler
maybe there is already a repository (or link collection) of datalad extensions?

Adina Wagner
here is a short overview: http://handbook.datalad.org/en/latest/extension_pkgs.html 

# Neuroimaging

# Systems and Behavioural Neuroscience

# Computational and Theoretical Neuroscience

# Molecular and Cellular Neuroscience

# Clinical Neuroscience

# Summary

