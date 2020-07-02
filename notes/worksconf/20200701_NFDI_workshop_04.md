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
  - alternative incentives should be implemented within the NFDI Neuro initiative giving an outlook on how proper RDM can help with the career.
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
  - the first round of students will have a hard time establishing proper RDM, but the second round of students can already work on collected data.
  - this initial collection step needs to be overcome.

- Michael Hanke
  - there is a point in additional incentives, but NFDI Neuro should remove the need for incentives and make RDM easy and training less costly.

- Karl Kafitz
  - students actually like RDM if they get the chance to train.
  - a problem are universities which do not give much support with respect to RDM in individual labs; there money is a problem, as soon as money is involved, universities get hesitant.

- Michael Denker
  - students are extremely motivated with respect to RDM, but usually are lacking the experience in RDM topics themselves since they come from different backgrounds.
  - funding and acknowledging RDM efforts are important.

- Julien Colomb
  - the DFG should be actively engaged in requiring incentives for grants with respect to RDM.


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
  - they are using DataLad with GIN. DataLad on its own is too complicated; access needs to be made easier for biologists.
  - Michael Hanke: just providing a GUI is not a solution, automatically extracting metadata from datasets and make them available should already help; interfaces for metadata should be developed to make required metadata entry low key as well. The Community needs to be engaged for tailored solutions to this end. NFDI Neuro should be the platform for it. Convenience and robustness need to be balanced.

- Stephan Hachinger, LRZ Graching
  - interested in contributing to RDM within the scope of NFDI Neuro; they already did some effort for writing adaptors to export metadata to search engines and offer capacity to write adaptors for NFDI projects as well.
  - is the NFDI planning to deploy Datalad on computing centers; how to best interact with NFDI in the next weeks;
  - Michael Hanke: NFDI Neuro will not visit every institute and deploy services, but will establish collaborations with institutes; so called transfer teams for the individual Task areas should be permanently reachable people available for institutes and data centers.

- Timo Dickscheid:
  - follow up on Julien Colomb; there is a gap between developers and analysts and people in a lab; within the lab there are already individual solutions.
  - Datalad makes sense and they ould like to use it, but it was too difficult for their Neuroanatomists to quickly learn and use.
  - agrees that a custom interface for user groups would make much sense; they are in the process of implementing one to put an entry-mask on top of Datalad and it works quite well.
  - the NFDI should also be a point of access to share these user interfaces.
  - Michael Hanke: the collaboration aspect in development is the proper approach; a common layer for collaborative development needs to be established via NFDI Neuro and made known to the experts within individual labs so they can participate and benefit.

- Lucia Melloni
    - they encounter problems in documenting complete metadata and to make them searchable; from their perspective community standards in metadata are required.
    - Michael Hanke: Datalad is dumb in the sense that it does not get in the way when collecting and providing data and metadata. NFDI Neuro should start with low quality metadata standards and build up from there to reduce the barrier. The researcher has to be rewarded somehow for entering high quality metadata. Datalad already provides a local search engine for entered metadata w/o the need for a database.

- Tamas Spisak (UKE Essen)
  - they are using Datalad and plan to use it for imaging data; how is the stance with respect to GDPR.
  - Michael Hanke: they are working with the Virtual brain cloud which provide an assessment of GDPR compliance of datasets; Datalad cannot provide GDPR compliance out of the box.

- Philip Tovote:
  - an NFDI Neuro marketplace is a very good idea; would NFDI Neuro provide a platform for this kind of self organized marketplace?
  - Michael Hanke: the answer has to be yes. NFDI Neuro should be the coordinating entity and has to provide this kind of service. But the groups have to be defined first and then talk about metadata. Start small and succeed by not aiming too high and delay.

- Julien Coulomb
  - NFDI Neuro infrastructure and Datalad: is this the only content or will there be other tools
  - Michael Hanke: infrastructure is a wide field and should not just be Datalad. The core purpose is not to consolidate everything into a single tool but to connect existing tools. The underlying infrastructure should be and stay independently extensible and as de-central as possible. If a new tool compared to Datalad emerges that is better capable of getting the job done, it should be used and be easy to switch.
  - Thomas Wachtler: as clarification: infrastructure is used in a general sense and not in the sense of specific tools.

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
  - before getting into sharing data within a network, problems need to be solved.
    - thinking at the level of lab structure is a nightmare for the IT department of an institute; there were hundreds of island solutions at the Charite; researchers did not care about standards so far.
    - Charite currently has an intermediate solution; everyone uses the omero standard and started to help with the development of omero plus for imaging data.
    - NFDI Neuro should think broader than the individual lab and collect information how other collaborations have solved this problem.
  - Michael Hanke: there should be as little development within NFDI Neuro itself as possible but should be the connection between existing solutions. NFDI Neuro should think big in terms of size of institutions but should not exclude small labs either.

- Lucia Melloni
  - should NFDI Neuro reach out to other institutions or solutions e.g. exnat.
  - Michael Hanke: German legislation is unique, but all other aspects should stay connected to other initiatives; surveys are part of the plan to identify tools in use and how to best support them.
  - the NIDM format is an international effort and NFDI Neuro imaging is in touch with them; no point in building something within Germany that already exists.

- Philip Boehn-Sturm
  - Neuroimaging is well documented and defined on the human side, but Institutions are important players. How will NFDI Neuro interact with the institutions.
  - Michael Hanke: labs AND institutions have to be pursued and it opportunities should be advertised on both levels what NFDI Neuro is doing. When solutions are built that make researchers more effective, then people will use them; once this is accomplished, institutes will use them as well. The grassroots approach will be the more dominant one within NFDI Neuro, but both approaches will be pursued.

- Rene Bernard
  - the oemero platform can do both; it requires additional expertise when introducing a general solution within a large institution. NFDI Neuro should provide both options; one for small labs and one for institutes.
  - Michael Hanke: there is a need to prioritise; surveys should first be done and the inquire is out there to be an active participant. It would be very good to already have an institute wide solution that could be introduced to NFDI Neuro.

- Philip Boehm-Sturm
  - it was mentioned that not much funding is available. There should be some cost involved to make NFDI Neuro sustainable. Are there any guidelines in how to write NFDI Neuro specific grant applications or how to include NFDI Neuro in grant applications?
  - Thomas Wachtler: for now lightweight approaches are pursued due to the current scope of NFDI Neuro. Small projects can be funded within NFDI Neuro, but larger projects need different funding as well.
  - Alexandra Stein: other funding schemes for projects can be appropriated and NFDI Neuro can and will support in getting them.
  - Michael Denker: in future it will be important to include in grants how to introduce developed tools on a broader scope which in turn will increase the funding in the long run.

## Chat
Michael Hanke: I completely forgot: There is a similar feedback document for the Task area neuroimaging https://tinyurl.com/nfdi-ta1 
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
  - when developing new techniques and methods or using emerging techniques, who will decide what "the" standard should be. How can a workflow be established on making decisions how to deal with an emerging technology.
  - Hansjoerg Scherberger: it should be decided bottom up and via a discussion a consensus will be reached.

- Julien Colomb
  - how far does NFDI Neuro want to go. 90% of people still use Excel; will they be approached and included?
  - Hansjoerg Scherberger: everyone should be included; if e.g. Excel is used, then it should at least be well documented how these files are to be interpreted and used.
  - Sonja Gruen: it is important to pick scientists up where they are; e.g. Juelich has developed a way to support CSV sheets (odmltables).

- Sen Cheng
  - many ideas are similar to INCF ideas; there is already previous work, but why has the INCF not solved these questions?
  - Hansjoerg Scherberger: an issue there was that the community was not properly included and projects have to be beneficial for many users.
  - Thomas Wachtler: this is a good observation; the NFDI Neuro ideas do not come out of the blue. INCF has tried solving similar problems in the past. Why did INCF not succeed by now? Because the addressed problems are hard ones and the topics where too diverse with respect to the available funding. NFDI Neuro does not provide that much funding either but it should be more focused with respect to both topics and audience within Germany. Through focus and funding it can succeed.
    - Sen Chen: would INCF agree with this observation.
    - INCF has achieved quite a lot in certain areas but compared to the original scope the achievements are underestimated. BIDS, Datalad and other approaches have their roots in INCF. So stating that INCF should have achieved more understates the actual accomplishments.
    - Hansjoerg Scherberger: Its lucky to have the INCF since NFDI Neuro can build on their experience and the problem of RDM is way clearer at this point in time than it was 10 years ago, in addition to more clear legal outlines.
    - Michael Denker: with respect to the INCF it is important to mention that the comparable small size of the community in Germany brings scientists closer together within the country. Even if NFDI Neuro is similar to the INCF, the focus of NFDI Neuro is more on the adoption of tools instead of thinking about which tools should be developed. With respect to standardisation: NFDI Neuro should not enforce standards of how to do things, but standards that work should be documented and guidelines should be available, and it should provide and be a forum to discuss one workflow via another.

- Lucia Melloni
  - brainlab e.g. has tried such an approach for some time. Bottom up is good, but it is also good to know what has worked in the past and what did not succeed. The Allen Brain institute has an amazing project due to extensive funding; NFDI Neuro could and should benefit from which approaches did not succeed for them in the past.
  - Hansjoerg Scherberger: very good point; it is necessary to learn from past "mistakes".
  - Alexandra Stein: the established connections by NFDI Neuro to existing networks should make this point very feasable.

- Severin Heumueller
  - are there already tools available for the community discussion and a workflow how to interact with and inform participants?
  - Hansjoerg Scherberger: a support team should be included and outreach should also be supported to help with specific problems; especially when setting up new techniques / software in a lab.
  - Michael Denker: also there is a need to overcome the deadlock that developers do not know whether their tool has problems in a specific use case; this platform should help provide low key feedback.
  - Severin Heumueller: how will this solution be marketed so that people will be aware of it? Are there better tools to reach people other than workshops or meetings?
  - Thomas Wachtler: information is also distributed via various mailinglists e.g. NWG; the first step was to reach people that are willing to participate and then grow, once enough people are NFDI Neuro participants or supporters.

- Karl Kafitz:
  - there is a problem with metadata; local officials are not happy with making data public and demand threefold documentation in paper form. This might even be different between political districts. Are there any efforts in this direction?
  - Hansjoerg Scherberger: usually it is fine to document day to day on a digital basis and do a printed and signed version at the end of an experiment (at least in Lower Saxony).
  - Karl Kafitz: it is problematic to do this kind of work basically twice, since it simply binds of resources.
  - Thomas Wachtler: a survey could be done over multiple locations and point the officials to different political districts where this kind of official documentation scheme works well.
  - Otto Witte: unfortunately basically all officials implement their own rules based on a common law.
  - Alexandra Stein: this should be taken up at a later point in time since it is a very important point.

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
- Alexandra Stein: all fields have their own RDM issues; what are the ones encountered in computational neuroscience.
  - Michael Denker: for computational neuroscience many models where developed and extensive data was harvested, but the problem was how these two could be connected. The technical level is a constant barrier between the computational scientists and the experimental scientists. NFDI Neuro should also work on reconciling these two disciplines so one can comment on the other from their own expertise.
  - Otto Witte: models require the connection to scientific data so the connection is essential.

- Stephan Rotter
  - students have to learn from each other. A PIs job is to bring them together. The NFDI Neuro platform should help people learn from each other and the idea of a marketplace is very helpful in this respect. A platform where things can be changed and also exchange and discussion of e.g. models can take place.

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
  - a lot of the discussed points are domain unspecific; could e.g. one general teaching concept be applied to all areas; to his knowledge an NFDI group specific for teaching exists, will NFDI Neuro interact with them.
  - Otto Witte: This particular NFDI group will not apply during the current NFDI round.
  - Hansjoerg Scherberger: advises against collaboration with another NFDI group since the users will be even more diverse than within the NFDI Neuro community.
  - Thomas Wachtler: this is a question for the community; there is a number of initiatives for general topics NFDI consortia e.g. for generic data service. The DFG decided during the first round to not to consider overarching but rather consider only "fachspezifische" requests.

- Karl Kafitz
  - with respect to the Madgeburg issues: as long as dealing within a building collaboration common data and metadata exchange is doable. With larger collaboration issues with metadata arise, the exchange of data will be a problem; labbooks and software distributers are not willing to help with exporting to open formats. Within the scope of the NFDI Neuro approaching vendors might be more effective.
  - Constanze Seidenbecher: this is a good point, vendors are not very willing to support other formats than their own.
  - Karl Kafitz: Omero is already a good starting point.

- Pavol Bauer:
  - the intersections of different steps in a workflow are important. How will grad students get from omero to using Datalad; this needs to be properly taught to be used.
  - Karl Kafitz: the neuroimaging community already has some strategies how to use and open up formats but these strategies should be shared and distributed to a broader .
  - Alexandra Stein: exchange with various consortia already exists to share this kind of information.

- Alexandra Stein: with respect to Constanze Seidenbacher; there was a workshop in Magdeburg on developed RDM strategies. NFDI Neuro wants to build up a repository on such strategies and bring participants together in future workshops.

- Julien Colomb
  - what should people write at the grant application level; e.g. what should they write in CRC grants; can NFDI Neuro raise the quality in grant writing as well?
  - Thomas Wachtler: it would be a good idea to enforce this.
  - Constanze Seidenbacher: a workshop in grant writing was already held; the participants profited a lot with respect to writing the non-scientific side.

- Sonja Gruen
  - from her experience the DFG is currently not asking for or evaluating Data management plans too much, but this should change soon and also should from her point of view.
  - Constanze Seidenbacher: in her experience some grants already failed due to a lacking or unsatisfying RDM plan.
  - Sonja Gruen: the DFG should be pushed to take more care about considering RDM plans.
  - Otto Witte: in many collaborative research center applications the RDM plan is already a very important point.
  - Philip Tovote: they had an application to the DFG where a not well developed RDM plan was criticised.

## Chat
Julien Colomb
So if we want to share grant application (and reviews from the DFG, maybe also documentation about how the infrastructure project ended up the way it did), what tool could we use? If this public information or do we want to keep it visible only to “us” (whoever us is) ?


# Clinical Neuroscience (Otto Witte, Jena University hospital)

- require a conversion tool and a viewer for the DICOM standard to open up the recorded data

## Comments and discussion
- Severin Heumueller:
  - Jena is part of the Smith initiative; does the initiative overlap with what has been discussed?
  - Otto Witte: yes and no. They will work with the initiative on the legal issue part. In principle they work with standard clinical data.
  Severin Heumueller: they collaborate with two different initiatives as well and problems from clinical data will be solved by the initiatives because Heumuellers group lacks the manpower.

- Alexandra Stein: where would the main intersection with NFDI4health be
  - Otto Witte: clinic studies outside of hospitals, several areas where NFDI4health does not deal with legal aspects but collect patient data. Here could be an overlap with the NFDI Neuro to not repeat work on anonymisation of data. NFDI4health is "Versorgungsforschung", they are very open for discussion and collaboration.

- Hansjoerg Scherberger: how much would imaging overlap with the Task area 2 - since clinical need anonymisation.
  - Otto Witte: in principle the acquired data are much more standardised since they are routinely and constantly collected. Maybe the recorded data and metadata can overlap with Task area 2 and save them some work.
  - Philip Tovote: this discussion is very similar to their grant proposal which contains intertwining human and animal data; the answers are complex; maybe these plans can also be shared with the community. The data repositories that are needed should remain in parallel for human and animals but should be aligned in terms of standards. The medical side is ahead in some respect since they have standards and rules that are currently still lacking in animal research; maybe these can be applied to animal research as well. In the long run a consolidation between these standards and also with the computational neuroscience Task area should take place.
  - Hansjoerg Scherberger: this is a very good answer and should be used in the grant proposal.
  - Philip Tovote: just not over-promise to standardise everything and remain realistic.
  - Otto Witte: a simple starting point is needed since the implementation will take quite some time.

- Constanze Seidenbecher
  - if changes are made to the standard patient data, are there any other stakeholders that need to be considered.
  - Otto Witte: not the stakeholders are the problem but the established techniques and hardware that are available; to convert from these data formats to open formats will take most of the time and effort.

- Daniel Guellmar
  - raises the question if a change in structure would make sense if Task areas - branches of neuroscience - do similar things and have similar problems. The disciplines within neuroscience should mix and not be separate like with the Task areas.
  - it is not that necessary to have a common platform to share data but more important to make the people aware that these data exists.
  - there should also be communication channels that are bidirectional and not full public.
  - Otto Witte: its true the Task area disciplines are not that different, but the used data formats are and it is important to focus the work to consolidate them.
  - Thomas Wachtler: the defined categories should not be seen as divisions but overlaps should be recognised. The fields are at different stages in data annotation and sharing and the gaps are large. The idea is to structure the consortium to fetch people where they are and work from there.
  - Michael Denker: the idea behind the consortium structure was that every community could recognise themselves in the consortium. The fields overlap strongly and the goal should be to move closer together.

- Julien Colomb
  - how can the common questions be asked and discussed in a common way; maybe in a next workshop it could be discussed how to make this best visible to the community.
  - Thomas Wachtler: very good suggestion to focus on specific topics. It would also be good to get the Task areas going.
  - Hansjoerg Scherberger: the main danger of failing would not be to develop tools, but not to achieve the user outreach because they don't understand the problems at hand or that they do not think the problems are important. Especially during the early stage NFDI Neuro should be close to the community. The biggest fear of failure is that the people are not picked up.

- Daniel Guellmar
  - the NFDI Neuro consortium will create something with a benefit; some technical or structural burdens will be lifted. But there are different branches in neuroscience and the consortium should aim for defining an arching minimal standard for all neuroscientific data to get scientists to think in a general structure and not only in their own specific format. Formats change. What would the minimum standard to develop be.
  - a platform should be community driven but heavily guided by the consortium. It should not just be a forum where everyone does what they please.

- Severin Heumueller
  - There are a lot of topics but not all can be addressed at the same time. How and by whom will prioritisation of issues happen?
  - Thomas Wachtler: it is important to focus and get things used. With respect to prioritisation: the more useful an aspect seems and where the community engages the most, the higher the priority it will have.
  - Michael Hanke: The reason for the workshops was to collect exports. If that was not enough, then more workshops are required to collect more exports that will participate.

- Julien Colomb
  - outreach to researchers is a big part of the idea, but there currently are no participating experts on teaching and outreach. How would RDM outreach work, since none of the people in the current NFDI Neuro that are experts. Also how should the problem be addressed that there are no experts in RDM. It is very difficult to get researchers engaged.
  - Otto Witte: elements of outreach are already available and NFDI Neuro should first of course stick to what already exists.
  - Hansjoerg Scherberger: bring experts together and to talk to each other. They can teach each other the best.
  - Karl Kafitz: the most important point is to tell colleagues about the worth of RDM. When trying to do solicitation, people will not react favorably. 
  - Severin Heumueller: it is important to get people to realize that RDM is science as well. There is a unified patient consent in clinical tests that the resulting data can also be used for science; it has taken much time and effort to get all counties in Germany to decide on a common form. There the problem is, that there are many experts, but they will all disagree amongst themselves. Here getting the experts together will not lead to an answer. How to deal in such a case.
  - Otto Witte: the medical informatics initiative did agree on a common patient form only recently for all of Germany.
  - Thomas Wachtler: its sufficient to convey current broadly used knowledge; teaching this knowledge is already better than not teaching at all. Solving these issues on a common and public forum is more likely to succeed in the long run.
  - Severin Heumueller: getting an agreement between large institutions is a hard problem in this case.

- Daniel Guellmar
  - the objective could be to accumulate all information in Germany for RDM in the neuroscience community; how is this currently done? As a task do a consensus building on the existing tools.
  - Michael Denker: the workshop focused on the specific Task areas, but there are several tasks that the teams have as homework to go in the direction not to solve specific problems but bring people together and give direct support on emerging projects. Teaching and training should not be distributed in clusters but should be done coordinated. The quality assessment is what the common standards are and then push and advocate the ones that have advantages. These tasks have to be done by the individual groups. 

## Chat
Anke Jaudszus
TA5 Clinical Neuroscience 
https://t1p.de/neuro-TA5 


# Summary and wrap up

- Thomas Wachtler:
  - use the presented google docs to get involved.
  - slides will be available via the NFDI web page; mailing list is also available via the NFDI page.
  - next week there is a general NFDI web conference.

- Julien Colomb:
  - it would be good to make a list and contact points within the task areas what should be done next.
  - Thomas Wachtler: first contact points are the presenters today - from there a scheme will be drafted.
