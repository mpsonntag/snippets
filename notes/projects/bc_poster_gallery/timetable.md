## Timetable Bernstein conference

- [BCOS] as a very first thing create a scibo; this is important
- [G-Node] copy all files (required images, example spreadsheets) to scibo
- [G-Node] create all required spreadsheets

- [BCOS] create conference entry on abstracts.g-node.org
- [BCOS] abstract submission opening
    - open abstract submission on abstracts.g-node.org
- [BCOS] abstract submission deadline
    - close abstracts submission on abstracts.g-node.org

### Until last week of July
- [BCOS] review abstracts
  - review abstracts
  - set states to accepted or rejected?
- [G-Node]
  - sort abstracts
  - upload sort order to abstracts.g-node.org
  - [new step?] provide BCOS with CSV of all abstracts - ideally already with poster upload codes
- [G-Node] prepare services at bc.g-node.org and posters.bc.g-node.org
    - [BCOS] check required categories
      - Main, Invited Talks, Contributed Talks, Posters, Workshops, Exhibition, Conference Information
    - [BCOS] check banners
      - [xyz] define format to exchange used images
      - [xyz] common URLs to check images
    - [BCOS] check texts on login, sign up and poster upload pages
      - [xyz] define format to exchange texts
    - [G-Node] update services according to required content changes

### Until first week of August
- [BCOS] provide Online poster sheet with all available abstract IDs to G-Node for Poster upload code generation
  -> this should be changed; include the poster upload codes already in the first data csv transfer from G-Node to BCOS
- [G-Node] add poster upload codes to the SciBo posters CSV tables
- [BCOS] finalize Poster order in SciBo posters CSV tables
- [G-Node]
  - create poster.json list with correct poster order and poster upload codes from Online sheet
  - enable poster upload page
  - provide poster upload page with the poster.json file
  - prepare email whitelist password on the upload page
  - send admin password for email whitelist to BCOS
- [BCOS] send acceptance emails to poster presenters including upload code
    - check email template below

### Until second week of August
- [BCOS] set all abstracts to "accepted" that are accepted. Only these will be available on the gallery
- [BCOS] fully prepare SciBo CSV tables for
    - Posters / Invited Talks / Contributed Talks
    - Workshops
    - Exhibition
- [BCOS] prepare "Conference Information" content
- [BCOS] repository registration whitelist
  - continuously upload email addresses of registered users via the whitelist page: https://posters.bc.g-node.org/uploademail
- [G-Node] create and upload repository content from SciBo CSV tables

### Week before conference ??
- [G-Node] officially close poster upload
- [G-Node] generate gallery content and upload to gallery

### During conference
- [BCOS] continuously update email whitelist
- [BCOS] continuously update vimeo links in SciBo CSV tables
- [G-Node] continuously update galleries from updated SciBo CSV tables

### 1 Month after conference
- [G-Node] final backup of the gallery content, log files and statistics
- [G-Node] switch repository to static page
- [G-Node] shut off gallery containers

# Addendum

## Repository templates

[xyz] check whether adding these here makes sense

## Email templates

### Poster acceptance

    Subject: Bernstein Conference [xyz 2021] - your poster upload

    Dear [xyz],
    
    here we provide you with the link to upload your poster to the repository:
    
    https://posters.bc.g-node.org/
    
    Your personalized password for the upload is: [xyz 9c56f4769f]
    
    Please upload your PDF and video URL by [xyz Sunday, Sep 19, 2021, 8 pm CEST]. The repository will open for all conference participants on [xyz Monday, Sep 20}].
    
    Posters sent via email will not be considered.
    
    PDFs: there is no special format required. You may choose the one, which works best for you in the online setting.
    
    Video teaser: you can either host it on a platform of your choice (e.g. Google Drive, Dropbox, etc.)) and upload the respective URL to the repository.
    Alternatively, we can host your video on our Bernstein Network Vimeo Channel.  In that case, please upload your video in MP4-format until [xzy Friday, Sep 17, 1 pm CEST] here:
    [xyz https://fz-juelich.sciebo.de/s/x35LFYw3TSVqlvK]
    
    Label your video-file: "yourposter#_lastname_video"
    
    Please do not forget to register for the conference:
    [xyz https://bit.ly/BC21_reg]
    
    For any questions, please do not hesitate to contact me.
    
    Best regards,
    [xyz]


### Poster number notification
Dear [xyz],

congratulations again on the acceptance of your abstract "Off- and on-site collaboration and publication: The G-Node Infrastructure Services for research data management" for a poster presentation at Bernstein Conference [YYYY].

Your abstract number: [xyz]
Please use this abstract number for your uploads to the conference repository.

Your poster session: You are scheduled for poster session [xyz - Day Month DD, HH:mm - HH:mm CEST.]
Your poster board: [xyz - xyz]
Please note that the poster board number is not equal to the abstract number!

Following are some information on how to present and prepare your poster. For any updates please also visit our website.

Poster presentation

After a long break, we will go back to a fully on-site, in-person experience. Posters should have a size of DIN A0 (841 x 1189 mm). They must be prepared in portrait aspect ratio.
To accommodate every poster, presentations will be distributed over a total of four poster sessions of 80 mins each. After your session has ended, please dismount the poster quickly to give the presenter in the next session the chance to start on time.

Poster mounting time is [HH:mm - HH:mm]

Dismounting time is [HH:mm - HH:mm].


Conference Repository

Additionally to the on-site presentation, posters will be on display in the Conference Repository. The repository will be available only to registered participants from the beginning of [Month until Day, MM DD]. This gives participants the opportunity to select their posters of interest ahead of time. Each poster will have its own landing page, including abstract, schedule, PDF and a link to a video introduction, if provided.

Please upload your poster as soon as possible to the conference repository (https://posters.bc.g-node.org/) using your personal upload-key provided in your acceptance email.

To profit the most from presenting your research, we also strongly encourage you to prepare a short video introduction of max. 3 minutes. Shortly explain what is exciting about your research and invite participants to join you during the live poster session. To record your video, we suggest a common and easy-to-use tool, e.g. Zoom. For more elaborate versions you may find some help here: https://obsproject.com/.

Videos can be hosted in the Bernstein Conference Vimeo channel and will be available for registered participants only. If you wish for your video to be hosted by us you must upload your video before [Day, Month DD, YYYY, HH:mm CEST]! Upload your video file here: https://fz-juelich.sciebo.de/s/[ID]

Preferred video format is *.mp4. File names must follow the naming scheme [AbstractNumber_FirstAuthor]. Other file names will not be considered.

If you have any questions, please reach out to us.
Kind regards,
[xyz]


### Conference registration

    [xyz] Add email text


### Required SciBo Spreadsheets

BC2X_TODO
BC2X_posters_talks
BC2X_workshops
BC2X_exhibition

### Required SciBo Folders

BC2X_resources
├── Banners
├── Topics
├── Exhibition_materials
├── Exhibition_images
└── Conference_Information

### Required images and banners

In Resources/Banners provide the following images, named and in the format as requested:

Name                                  format      ideal dimensions          used at
BC_Header_contributed.jpg             jpg         4724x1063 px              https://bc.g-node.org/BernsteinConference/ContributedTalks/wiki
BC_Header_exhibition.jpg              jpg         4724x1063 px              https://bc.g-node.org/BernsteinConference/Exhibition/wiki
BC_Header_info.jpg                    jpg         4724x1063 px              https://bc.g-node.org/BernsteinConference/ConferenceInformation/wiki
BC_Header_invited.jpg                 jpg         4724x1063 px              https://bc.g-node.org/BernsteinConference/InvitedTalks/wiki
BC_Header_posters.jpg                 jpg         4724x1063 px              https://bc.g-node.org/BernsteinConference/Posters/wiki
BC_Header_workshops.jpg               jpg         4724x1063 px              https://bc.g-node.org/BernsteinConference/Workshops/wiki
BC_login_banner.jpg                   jpg         4724x1063 px              https://bc.g-node.org/BernsteinConference/Main/wiki
Kachel_ConferenceInformation.jpg      jpg         300x180 px                https://bc.g-node.org/BernsteinConference/Main/wiki
Kachel_ContributedTalks.jpg           jpg         300x180 px                https://bc.g-node.org/BernsteinConference/Main/wiki
Kachel_Exhibition.jpg                 jpg         300x180 px                https://bc.g-node.org/BernsteinConference/Main/wiki
Kachel_InvitedTalks.jpg               jpg         300x180 px                https://bc.g-node.org/BernsteinConference/Main/wiki
Kachel_Posters.jpg                    jpg         300x180 px                https://bc.g-node.org/BernsteinConference/Main/wiki
Kachel_Workshops.jpg                  jpg         300x180 px                https://bc.g-node.org/BernsteinConference/Main/wiki

In Resources/Topics provide the following images, named and in the format as requested:

Name                                  format      ideal dimensions          used at
blue.png                              png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
darkblue.png                          png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
green.png                             png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
grey.png                              png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
lightblue.png                         png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
orange.png                            png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
purple.png                            png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
red.png                               png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
salmon.png                            png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
turquoise.png                         png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics
yellow.png                            png         300x169 px                https://bc.g-node.org/BernsteinConference/Posters/wiki/Topics

blue-wide.png                         png         1000x150 px               as assigned to topic
darkblue-wide.png                     png         1000x150 px               as assigned to topic
green-wide.png                        png         1000x150 px               as assigned to topic
grey-wide.png                         png         1000x150 px               as assigned to topic
lightblue-wide.png                    png         1000x150 px               as assigned to topic
orange-wide.png                       png         1000x150 px               as assigned to topic
purple-wide.png                       png         1000x150 px               as assigned to topic
red-wide.png                          png         1000x150 px               as assigned to topic
salmon-wide.png                       png         1000x150 px               as assigned to topic
turquoise-wide.png                    png         1000x150 px               as assigned to topic
yellow-wide.png                       png         1000x150 px               as assigned to topic

icon-blue.png                         png         27x15 px                  as assigned to topic
icon-darkblue.png                     png         27x15 px                  as assigned to topic
icon-green.png                        png         27x15 px                  as assigned to topic
icon-grey.png                         png         27x15 px                  as assigned to topic
icon-lightblue.png                    png         27x15 px                  as assigned to topic
icon-orange.png                       png         27x15 px                  as assigned to topic
icon-purple.png                       png         27x15 px                  as assigned to topic
icon-red.png                          png         27x15 px                  as assigned to topic
icon-salmon.png                       png         27x15 px                  as assigned to topic
icon-turquoise.png                    png         27x15 px                  as assigned to topic
icon-yellow.png                       png         27x15 px                  as assigned to topic

The latest Topic - color assignment was:

    "Networks, dynamical systems": "yellow",
    "Data analysis, machine learning, neuroinformatics": "blue",
    "Learning, plasticity and memory": "red",
    "Sensory processing and perception": "green",
    "Attention, reward, decision making": "orange",
    "Behaviour and cognition": "lightblue",
    "Brain disease, network dysfunction and intervention": "turquoise",
    "Single neurons, biophysics": "grey",
    "Motor control, movement, navigation": "purple",
    "Neurotechnology": "salmon",
    "Other": "darkblue",


## common registration problems

"I cannot register with the repository service"
- email address not whitelisted yet; check if email address is in whitelist upload list
- different email used than with the conference registration; ask user to use the appropriate email address

"I cannot log into the repository service"
- requires registration with the repository service; ask to register with the appropriate email address

"I cannot log into the repository service, I get the message 'registration code expired'"
- registration activation link clicked twice; user should already be activated; ask to log in or reset password
