# Potential changes notes for current files

- g-node.1e7756.xml
  - not-usefull funding reference (empty DFG award number after full DFG entry)

        <fundingReference>
          <funderName>DFG</funderName>
          <awardNumber>SFB889</awardNumber>
        </fundingReference>
        <fundingReference>
          <funderName>DFG</funderName>
          <awardNumber></awardNumber>
        </fundingReference>

- g-node.5a4628
  - probably not our fault, there seems to be a typo (`Helth`):

        <fundingReference>
          <funderName>Kids Brain Helth Network</funderName>
          <awardNumber></awardNumber>
        </fundingReference>

- g-node.5b08du
  - empty language tag
  - empty version tag

- g-node.6a0d94
  - Typo in a title (`fied`)

        <titles>
          <title>Local fied potential dataset: fronto-striatal oscillations predict vocal output in bats  </title>
        </titles>

- g-node.7a5020
- repeating subjects

        <subjects>
          <subject>delay discounting, win-stay, lose-switch, perseveration, reversal learning, perceptual uncertainty</subject>
          <subject>win-stay, lose-switch</subject>
          <subject>perseveration</subject>
          <subject>reversal learning</subject>
          <subject>perceptual uncertainty</subject>
        </subjects>

- g-node.9c0912
 - again as in the related doi above, there seems to be a typo (`Helth`):

        <fundingReference>
          <funderName>Kids Brain Helth Network</funderName>
          <awardNumber></awardNumber>
        </fundingReference>

- g-node.57a01e
  - author affiliations contain not escaped ampersand for multiple authors:

          <creatorName>Sehara, Keisuke</creatorName>
          <creatorName>Nashaat,  Mostafa A.</creatorName>
          <creatorName>Oraby, Hatem</creatorName>
          <creatorName>Larkum, Matthew E.</creatorName>
          <creatorName>Sachdev, Robert N.S.</creatorName>
          <affiliation>Institut für Biologie, Neurocure Center for Excellence, Chariteplatz 1 / Virchowweg 6, Charité Universitätsmedizin Berlin &amp; Humboldt Universität, Berlin, 10117 Germany.</affiliation>

  - author contains an empty ORCID entry

        <creator>
          <creatorName>Dominiak, Sina E.</creatorName>
          <nameIdentifier schemeURI="https://orcid.org/" nameIdentifierScheme="ORCID"></nameIdentifier>
          <affiliation>Institut für Biologie, Neurocure Center for Excellence, Chariteplatz 1 / Virchowweg 6, Charité Universitätsmedizin Berlin &amp; Humboldt Universität, Berlin, 10117 Germany.</affiliation>
        </creator>

- g-node.80dd9a

  - unescaped ampersand in description `...P Barsi & LR Kozák</description>`
  - typo in subject:

        <subject>Neurorimaging</subject>

- g-node.97bc14
  - unescaped 'lesser than' in abstract description `...luminance < 0.01 cd/m2...`

- g-node.134e2c
  - unescaped ampersand in title `Data for Gill & Chiel 2020:`

- g-node.3730d0
  - unescaped ampersand in author affiliation: `Histology & Research Laboratory`

- g-node.6269c2
  - unescaped ampersand in author affiliation:

          <creatorName>Soltanian-Zadeh, Hamid</creatorName>
          <affiliation>University of Tehran &amp; Henry Ford Health System</affiliation>

- g-node.52349d
  - unescaped ampersand in fundingReference

        <fundingReference>
            <funderName>National Key R&amp;D Program of China.2017YFC0840100 and 2017YFC0840106</funderName>

- g-node.b56be0
  - unescaped ampersand in both descriptions: `...Soyman & Vicario...`, `...Soyman, E. & Vicario...`

- g-node.d9dd71
  - size is `0 B`

- g-node.d315b3
  - unescaped ampersand in description `...Abraham Betancourt &amp; Hugo Merchant...`

- g-node.e520bb
  - lower case authors name: `<creatorName>chen, xi</creatorName>`

- g-node.hnj28q
  - empty relatedIdentifiers tag
  - empty language tag
  - empty version tag
  - size `0 B`

- g-node.m9hpkr
  - empty language tag
  - empty version tag

- g-node.o1g64d
  - empty relatedIdentifiers tag
  - empty language tag
  - empty version tag
  - size `0 B`

- g-node.t6vbz9
  - empty language tag
  - empty version tag

- g-node.vd9c21
  - empty language tag
  - empty version tag
