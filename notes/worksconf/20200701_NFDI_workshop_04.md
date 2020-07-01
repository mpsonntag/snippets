# NFDI Neuro workshop 2020.07.01

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

## Discussion and comments
- Phillip Tovote
  - the community approach is very appreciated
  - sections (task areas) are a good idea
  - how can the community motivate itself for the task at hand. The system is still mainly driven by the impact factor and there is no reward for proper RDM and sharing might be even counter productive for a PhD's or a postdoc's career.
  - this is a complex, philosphical discussion but should be held.
  - alternative incentives should be implemented into the NFDI Neuro initiative giving an outlook on how proper RDM can help with the career.
  - Thomas Wachtler:
    - scientists are more effective with proper RDM. By aggregating a community it will be easier to overcome the immediate reward barrier.
    - with respect to open data there is no established credit system yet, but journals already support data publications and credits for data publication will come in time.
- Otto Witte
  - many data repositories are too much work and too much documentation is required.
  - more positive impulses for data publications are required.
  - funded research must demand open data publication.
- Lucia Melloni
  - NFDI Neuro should be used to develop guidelines which can work as an incentive for a community.
  - their lab is working in a large collaboration and RDM is an issue; the data sharing is difficult and the rewards for limited positions like PhDs are not available; they need to profit in some way.
  - these rewards need to be actively developed.
- Sonja Gruen:
  - first round of students will have a hard time establishing proper RDM.
  - but the second round of students can already work on the collected data.
  - this initial collection step needs to be overcome.
- Michael Hanke
  - there is a point in additional incentives.
  - but NFDI Neuro should remove the need for incentives and make the RDM so easy to make training less costly.
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

## Discussion and comments
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


# Neuroimaging (Michael Hanke)

## State of RDM in Neuroimaging
- there already are established standards in Neuroimaging; NIFTI and DICOM; BIDS
- good basis, but not extensive enough; majority of studies are deemed not reproducible.
- size of datasets is increasing, but it gets a problem to even access this amount of data to run analysis on it.
-> an aim of NFDI Neuro should also be to address the question to develop and establish means to access this kind of large data sets.

## Measures required to Improve RDM in Neuroimaging
- NFDI should not be Neuroscience in Germany but a voice in Neuroscience from Germany.
- M4: provide recommendations and inform about best-practices on legal aspects of acquiring human subject data
- M5: develop data harmonization tools across modalities, centers and studies.
- M6: automated extraction tools of data and metadata and conversion to common data structure
- M7: Training, on demand help and documentation

## How participants and supporting community members profit in practice
- NDFI Neuro imaging group should first collect the workflows that individual labs use and collect the problems that arise; use this to develop and publish best practices.

## Discussion
- Rene Bernard (Charite)
  - before getting into sharing in a network problems need to be solved
    - thinking in lab structure is a nightmare for the IT -> hundreds of island solutions at the Charite; researchers did not care about standards so far.
    - Charite has an intermediate solution - everyone uses the omero? standard and started to help with the development of omero plus.
    - NFDI Neuro should think broader than the individual lab and collect information how other collaborations have solved this problem.
  - MHanke: there should be as little development within NFDI Neuro itself. NFDI Neuro should be the connection between existing solutions. NFDI Neuro should think big in terms of size of institutions but should not exclude small labs either.
- Lucia Melloni
  - should NFDI Neuro reach out to other institutions eg exnat
  - MHanke: German legislation is unique, but all other aspects should stay connected to other initiatives; surveys are part of the plan to identify tools in use and how to best support them
  - NIDM format is an international effort and NFDI Neuro imaging is in touch with them; no point in building something within Germany that already exists
- Philip Boehn-Sturm
  - Neuroimaging is well on the human side, but Institutions are important players. How will NFDI Neuro interact with the institutions.
  - MHanke: labs and institutions have to be pursued. Advertise opportunities to learn what NFDI Neuro is doing. When solutions are built that make researchers more effective, then people will use it. In this case the institutes will use them as well. The grassroots approach will be the more dominant one but both approaches will be pursued.
- Rene Bernard
  - oemero platform can do both - requires additional system when setting it up in a large institution. NFDI Neuro should have both pathways - one for small labs and one for institutes.
  - MHanke: need to prioritise -> surveys, be an active participant, it would be very good to already have an institute wide solution that could be introduced to NFDI Neuro
- Philip Boehm-Sturm
  - it was mentioned that not much funding is available. There should be some cost involved to make it sustainable. Are there ideas about workflows, how should that be written in grants - are there any quidelines in how to write this in grants is there support?
  - TWachtler: pursue lightweight approaches since we cannot handle it. Small projects can be funded within NFDI Neuro, but larger projects cannot be funded.
  - A Stein: other funding schemes for projects can be appropriated and NFDI Neuro can help there
  - M Denker: in future it will be important to show in grants how to introduce tools on a broader scope which in turn will increase the funding in the long run.

## Chat
Michael Hanke: I completely forgot: There is a similar feedback document for the task area neuroimaging https://tinyurl.com/nfdi-ta1 
(sorry for the late notice)


# Systems and Behavioural Neuroscience (Hansjoerg Scherberger)

- over time behavioral and ephys experiments have become more and more complex
- the metadata to document how the actual experiment was performed and analysed have become very hard to document as well
- storing data and metadata is problematic, analysis is non-standard

Analysis itself has problems
- many diverse tools used in non-standard ways.
- metadata is missing quite often.

NFDI Neuro can help with
- dev of platform independent data formats
- handling of metadata
- workflow standardisation
- ability to re-analyze and re-use data sets years later

- with any of the developments on the side of NFDI Neuro feedback from actual labs is essential
- there is funding available for development together with labs

## Comments and discussion
- Philip Tovote
  - pushing the envelop - when developing new techniques and methods or using emerging techinques, who decides what the standard should be. How can a workflow be established to decide how to deal with an emerging technology
  - HScherberger: it should be decided bottom up and via a discussion a consensus should be reached.
- Julien Colomb
  - how far does NFDI Neuro want to go. 90% of people still use Excel; will they be approached and included?
  - HScherberger: everyone should be included; if e,g, excel is used, then it should at least be documented
  - SGruen: pick people up where they are; in Juelich CSV sheets are supported (odmltables)
- Sen Cheng
  - many ideas are similar to INCF ideas. So there is already previous work, but why has not INCF accomplished the questions already?
  - HScherberger: a problem there was that the community was not properly included and the projects have to be beneficial for many users.
  - TWachtler
    - good observation; the NFDI Neuro ideas do not come from nowhere. INCF has tried this in the past. Why does INCF did not succeed by now? because its a hard problem and the topics where too diverse for the available funding. NFDI Neuro does not provide that much funding either but it should be more focused on both topics and audience within Germany. Through focus and funding it can succeed.
    - SChen: would INCF agree with this observation
    - INCF has acchieved quite a bit in certain areas but compared to the original scope it can be underestimated. BIDS, Datalad and other approaches have their roots in INCF. So stating that INCF should have achieved more understates the achievements.
    - HScherberger: Lucky to have INCF since NFDI Neuro can build on it and the problem of RDM is way more clear at this point in time than it was 10 years ago, in addition to more clear legal outlines.
- MDenker
  - INCF: important to mention that small size of community brings scientists closer together. Even if similar to INCF, the focus of NFDI Neuro is more on the adoption of tools instead of thinking bout which tools should be done.
  - standardisation: NFDI Neuro should not be the standard of how to do things, but the things that work should be documented and guidelines should be available, plus a forum to discuss one workflow via another
- Lucia Melloni
  - brainlab e.g. has tried this for some time. bottom up is good, but it is also good to know what has work and what has not. allen institute has an amazing project due to funding and we could benefit from what did not work for them.
  - HScherberger: very good point; it is necessary to learn from past "mistakes".
  - AStein: the established connections to existing networks should make this very possible.

- Severin Heumueller
  - are there already tools for the community discussion and a workflow how to interact and informat participants?
  - HScherberger: a support team should be included and outreach should also be supported to help with specific problems especially when setting up new techniques / software in a lab
  - MDenker: need to overcome the deadlock that a developer does not know whether the tool has problems in a specific use case - the platform should help provide low key feedback
  - SHeumueller: how will this solution be marketed so that people will be aware? are there better tools to reach people other than workshops or meetings?
  - TWachtler: distributed via NWG mailinglists; first step was to reach people that are willing to participate and then grow once enough people are already supporters.

- Karl Kafitz:
  - problem with metadata - officials are not happy with making data public and demand threefold documentation and in paper form. which might also be different between political districts. are there any efforts in this direction?
  - TWachtler: on paper is a problem.
  - HScherberger: its ok to document day to day and do a printed and signed version at the end of the experiment (in lower saxony).
  - KKafitz: it is problematic to do work in duplicates, it simply binds tons of resources.
  - TWachtler: could do a survey over multiple locations and point the officials to different locations where it works as well.
  - Otto Witte: every official does their own rules based on a common law
  - A Stein: this should be taken up since it is a very important point.

## Chat
Hans Scherberger: TA2 Systems & Behavioral Neuroscience comments: https://docs.google.com/document/d/1tJqNDFdmCW840Z2GhRIcM2r-ySf4IHx4p9eJ5mXuAmY/edit?usp=sharing

Julien Colomb
excel has (unfortunately) to be added to that list

Michael Hanke
NCF has also tried things that we now know did NOT work. And that is very important knowledge. 
And indeed, there would be no DataLad without INCFs initiatives and working groups-- the concepts present in that community shaped and do shape the present efforts.

Julien Colomb
maybe of interest for working with administration: https://www.labfolder.com/features/#Compliance 


# Computational and Theoretical Neuroscience (Michael Denker)

Focus areas for Computational Neurosicence
- I: Best practices for model description and simulation outcomes
- II: Simulation, analysis, validation workflows and provenance
- III: Simplifying model validation and verification of simulations

## Focus I
- really hard to redo a model simulation from a paper
- how can an abstract modeling language description be reconciled with a repository??

- models have been standardized in physics -> how can neuronal network models be standardized in a similar way?

## Focus II
- analysis is quite heterogeneous
- how can analysis be made comparable across tools
-> build universal workflows across different analysis' to enable comparison across tools and methods.

- NFDI Neuro could help in organising these workflows - Marketplaces for tools and workflows.

## Focus III
- NFDI Neuro is to promote best practices to set up simulation environments and standards to compare across different models.
- metadata that is done in Task Areas 1 and 2 should fit the one in Task Area 3 ... NFDI Neuro should already bridge that gap automatically and ensure that not another gap is opened.

## Comments and documents
- A Stein: all fields have their own RDM issues what are the ones for comp neuro
  - MDenker: for comp neuro a lot of models where developed and tons of data harvested, but how could these two be connected. The technical level is standing between the comp scientists and the experimental scientists. So NFDI Neuro should also work on reconciling these two disciplines so one can comment on the other from their own expertise.
  - Otto Witte: models require the connection to scientific data so the connection is essential
- Stephan Rotter
  - students have to learn from each other. PIs job is to bring them together. The NFDI Neuro platform should help people learn from each other. The idea of marketplace is very helpful in this respect. A platform where things can be changed and also exchange and discussion of e.g. models can take place.


## Chat
Michael Denker
https://tinyurl.com/nfdi-compneurosci

# Molecular and Cellular Neuroscience (Constanze Seidenbecher, Pavol Bauer, LIN Magdeburg)

- OME bio-format library .. can read more than 100 imaging format and save in an annotated format (omero).
- combined physiological and behavioral data
  - metadata problem - live in different domains hard to collect it in a standardised way.



- a grant working group would be very good and could be a magnet for users which then might check out the forums for other areas as well.

## Comments and discussion
- Julien Colomb
  - a lot of the discussed points are domain unspecific; could e.g. one general teaching concept for all areas.; there was an NFDI specific for teaching and will NFDI Neuro interact
  - Otto Witte: This group will not apply in this NFDI round
  - HScher: would advise against collaboration with another NFDI group since the users will be even more diverse than within the NFDI Neuro community
  - TWachtler: question for community ... number of initiative for NFDI consortia for general topics e.g. generic data service. DFG decided on the first round not to consider overarching but rather consider only fachspezifische requests.
- Karl Kafitz
  - re madgeburg issues: as long as dealing within a building collaboration its doable. but with larger collaboration issues with metadata arise, the exchange of data will be a problem - labbooks and software distributers are not willing to help with exporting to open formats. Within the scope of the NFDI approaching vendors might be more effective.
  - CSeidenbecher: good point, vendors are not very willing to support other formats.
  - KKafitz: Omero is already a good starting point
- Pavol Bauer:
  - the intersection of different steps in a workflow are important. how does a grad student get from omero to using datalad - this needs to be properly taught to be used
  - KKafitz: neuroimaging community already has some strategies how to open up formats but the strategies should be shared.
  - AStein: there already are connections to various consortia to share this kind of information.
- AStein: CSeidenbacher - there was a workshop on already developed RDM strategies. NFDI Neuro wants to build up a repo on strategies and bring the participants together.
- Julien Colomb
  - what should people write at the grant application level. what should they write in CRC grants - can NFDI Neuro raise the quality in grant writing as well?
  - TWachtler: would be a good idea to enforce this.
  - CSeidenbacher: held a workshop in grant writing - they profited very much about writing the non-scientific side.
- Sonja Gruen
  - DFG is asking for Data management plan? it is not really relevant for funding right now, but it should change soon.
  - CSeidenbacher: some grants failed due to lacking RDM plan.
  - SGruen: will push the DFG to take more care about considering RDM plans.
  - OWitte: in many collaborative research centers applications the RDM plan is already a very important point.
  - PTovote: had application with DFG where a not well developed RDM plan was criticised.

## Chat
Julien Colomb
So if we want to share grant application (and reviews from the DFG, maybe also documentation about how the infrastructure project ended up the way it did), what tool could we use? If this public information or do we want to keep it visible only to “us” (whoever us is) ?


# Clinical Neuroscience (Otto Witte, Jena University hospital)

- require a conversion tool and a viewer for the DICOM standard to open up the recorded data

## Comments and discussion
- Severin Heumueller:
  - Jena part of Smith initiative; does the initiative overlap with what has been discussed?
  - OWitte: yes and no. Will work with them on the legal issue part. In principle they work with standard clinical data.
  SHeumueller: work with 2 different initiatives as well and problems from clinical data will be solved by them because SHeumueller lacks the manpower.
- AStein: where would be the main intersectio nwith NFDI 4 health
  - OWitte: clinic studies outside of hospitals, several areas where they deal with patients, do not deal with legal aspects but with patients. Here could be an overlap with the NFDI Neuro to not repeat work on anaonymising data. NFDI for health is versorgungsforschung. They are very open for discussion and collaboration.
- HansScherberger: how much would would imaging overlap with the task 2 - since clinical need anonymisation.
  - OWitte: in principle the acquired data are much more standardised since they are routinely taken. maybe the recorded data / metadata can overlap with task 2.
- Philip Tovote
  - group discussion very similar to their grant proposal where intertwining person and animal data - the answers are complex; maybe these plans can also be shared with the community. the data repos that are needed should be in parallel for human and animals but should be aligned in terms of standards. the medical side are ahead in some respect since they have standards and rules that are lacking in animal research - maybe these can be applied to animal research as well. in the long run consolidate these standards also with the computational neuroscience task group.
  - HScherberger: very good answer and should be used in the grant proposal.
  - PTovote: just not overpromise to standardise everything and remain realistic.
  - OWitte: need to be a simple start since the implementation will take quite some time.
- Constanze Seidenbecher:
  - if we deal with patient data - if changes are made to the standard data, are there any other stakeholders that need to be consulted
  - OWitte: not the stakeholders are the problem but the established techniques and hardware that are available - to convert from these data formats to open ones will take most of the time.
- Daniel Guellmar:
  - change structure if task areas - branches of neuroscience do similar things and have same problems. change the view on that; defining standard is one thing but enforces to push discussion how to share data and make it visible. it is not that necessary to have a common platform to share but at least make the people aware that these data exists. there should be channels that are bidirectional and not full public as well. The disciplines within neuroscience should mix and not be separate like with the task areas
  - OWitte: its true the worlds are not that different, but the used formats are and it is important to
  - TWachtler: the defined categories should not be seen as divisions and overlaps should be recognised. but the fields are at different stages in data annotation and sharing and the gaps are large. the idea is to structure the consortium to fetch people where they are and work from there and help fields to work from each other from there.
- Michael Denker
  - the idea was to structure the consortium in a way so that every community would recognise them in the consortium. the fields overlap strongly and the goal should be to move closer together.
  - OWitte: agreed, in the long
- Julien Colomb:
  - how can the common questions be asked and discussed in a common way - maybe in a next workshop it could be discussed how to make this best visible to the community
  - TWachtler: very good suggestion to focus on specific topics and might be helpful. also good to get the working groups starting.
  - Hans Scherberger: the main thing to fail would not be to dev the tools, but not reaching out to the users because they dont understand it or that they do not think its important. especially in the beginning it should be close to the community. biggest fear of failure: we do not pick up the people.
- Daniel Guellmar
  - consortium will create something with a benefit - some technical or structural burdens will be lifted. but different branches in neuroscience we should aim for defining an arching minimal standard for all neuroscience data e.g. did not think about modeling. what is the overarching structure to cover all neuroscientific data to get people to think in a general structure and not only in their own specific format. formats change. what would be the minimum standard to develop.
  - a platform should be community driven but heavily guided by the consortium. it should not be just a forum where everyone does what they please.
- Severin Heumueller:
  - prioritisation of issues: how will this happen? lot of topics but not all can be adressed at the same time. how will we prioritised? who guides it.
  - OWitte: we cannot describe the while world and not neuroscience. with the task areas it is like a matrix depending how you look at it.
  - TWachtler: also important to focus and get things used. with respect to prioritisation: the more useful it seems the higher the priority it will have. which also includes where the community engages the most.
  - MHanke: indeed. in the middle of priorisation. stick to the things that we know. The reason for the workshops was to collect exports. If that was not enough do more workshops to collect more exports that will participate.
- Julien Colomb
  - outreach to researchers is a big part of the idea, but there are no experts on teaching. how would RDM outreach work, since none of the people in the current NFDI Neuro that are experts. How to address this problem that there are no experts in RDM. It is very difficult to get researchers engaged.
  - OWitte: there are elements of outreach already there and we should stick to the elements that are already there.
  - HScherberger: bring experts together and to talk to each other. They can teach each other the best.
  - Karl Kafitz: most important point is to tell the colleagues about the worth of RDM. when trying to solicitate, people will not react favorably. 
  - Severin Heumueller: get it into peoples heads that RDM is science as well. the unified patient consent that data can also be used for science, it has taken tons of times to get all countries in germany to decide on a same form. there the problem is, there are many experts, but they will all disagree amongst themselves. here getting the experts will not lead to an answer. how to deal in such a case.
  - OWitte: the medical informatics initiative did agree on a common patient form only recently for all of Germany.
  - TWachtler: its sufficient to convey what everyone already knows and teaching what each knows is already better than not teaching at all. and solving it together is better in the long run.
  - SHeumueller: puts the point that getting an agreement between large institutions which are currently not solvable.
- Daniel Guellmar
  - what if the objective would be to accumulate all information in Germany for RDM in the neuroscience community; how is this currently done? as a task do a consensus building on the existing tools.
  - MDenker: the workshop focused on the specific task areas, but there are several tasks that the teams have as homework to go in the direction not to solve specific problems but bring people together and give direct support on emerging projects. teaching and training should not be distributed in clusters but should be done coordinated. quality assessment: what are common standards, then push and advocate the ones that have advantages. these tasks have to be done by the individual groups. 

## Chat
Anke Jaudszus
TA5 Clinical Neuroscience 
https://t1p.de/neuro-TA5 


# Summary and wrap up

- Thomas Wachtler:
  - use the presented google docs to get involved.
  - slides will be available via the NFDI web page; mailing list is also available via the NFDI page.
  - next week there is a general NFDI web conference


