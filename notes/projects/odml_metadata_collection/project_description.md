# Project description: odml metadata collection

## General project description

Repository at https://gin.g-node.org/msonntag/metadata-collection:

Used to document and collect odML from odML and NIX files from GIN repositories, convert them to the latest odml version and prepare them for conversion to RDF.

The original odml and NIX files can be found in the raw folder. This folder also contains links to where the files where originally collected from and contains name mappings in case ambiguous file names had to be changed to make them unique.

odml files converted to the latest version and odml files extracted from NIX files can be found in folder processed/odml-v1-1.

## More detailed description of metadata files scraping from repositories


These files where collected from public repositories published on GIN.

The table below collects the original names and full paths of the collected files, the updated file name and whether the file was part of a DOI or not.

All files are collected in this folder, therefore the individual collected files have to renamed using the following scheme to ensure the files can be unambiguously saved and their original repository identified:

[GIN-User]__[Repository-Name]_[Original_filename]_###.[original_file_extension]

GIN-User and Repository-Name combined should not exceed 30 characters which should be sufficient to identify the original repository from the file name.

E.g. the odml file at repository https://gin.g-node.org/doi/efish_locking/src/master/2014-05-21-ab/metadata.xml would be renamed to doi__efish_locking_metadata_001.xml.

| Raw File name | Full path | Updated file name | DOI  |
| ------------- | --------- | ------------------| ---- |
| metadata.xml | https://gin.g-node.org/doi/efish_locking/src/master/2014-05-21-ab/metadata.xml | doi__efish_locking_metadata_001.xml | https://doi.org/10.12751/g-node.6953bb |
| stimulus-metadata.xml | https://gin.g-node.org/doi/efish_locking/src/master/2014-05-21-ab/stimulus-metadata.xml | doi__efish_locking_stimulus-metadata_001.xml | https://doi.org/10.12751/g-node.6953bb |

## Detailed suggested workflow description (german)

Jetzt zum naechsten Projekt. Das ist relativ wichtig fuer uns und geht eher in Richtung Datenkuration und weniger in Richtung Programmierung, aber ich habe mich bei der Projektstrukturierung bemueht es so zu gestalten, dass es fuer dich hoffentlich trotzdem spannend bleibt. Es ist auch tatsaechlich ein richtiges kleines Projekt das dir ueberlassen ist und beinhaltet dadurch eben nicht nur Programmierung.

Das Ziel ist, fuer eines unserer langfristigeren Projekte (odML RDF) bereits verfuegbare odml Metadaten aus allen auf GIN (gin.g-node.org) publizierten Datensaetzen zu sammeln, in die neueste odml Version zu bringen und letzten Endes nach RDF zu konvertieren. Dazu ist es notwendig, die publizierten GIN Repositories nach NIX und odML files zu durchsuchen, herunterzuladen und in einem dafuer vorgesehenen Repository: https://gin.g-node.org/msonntag/metadata-collection gut dokumentiert zu sammeln.

Dieses Repository enthaelt READMEs, die genauer beschreiben wie und wo Dateien gesammelt werden sollen. Ich muss dich da noch als Collaborator hinzufuegen, bitte schick mir dazu deinen GIN Username.

Damit die Suche nach passenden Files auf GIN nicht zu langweilig wird, haette ich vorgeschlagen, dass du folgendermassen vorgehst:
Geh konsequent jeden Tag durch 5 Repos durch und pruefe, ob
- NIX files enthalten sind, die sollte man anhand der Dateiendung ".nix" gut erkennen koennen.
- odML files enthalten sind. Dazu muss man all XML files oeffnen (ueber die GIN weboberflaeche oeffnen reicht) und pruefen, ob der Inhalt odML ist.
- jedes gepruefte Repository in die Tabelle im Root-README eintragen.
- die Daten zu allen gefundenen NIX und odML files aufnehmen, in `raw/README.md` eintragen und entsprechend hochladen.
- generell beginne zuerst mit allen Repositories des DOI Users (https://gin.g-node.org/doi).
- wenn du durch diese durch bist, geh auch zu anderen Repositories ueber, aber lass diejenigen aus, die bereits einen DOI haben.
- Repositories die offensichtlich Tests und keine Datenpublikationen sind und daher fuer unsere Metadatensammlung nicht von Interesse sind, koennen ausgenommen werden. Als Beispiel: NeuralEnsemble/ephy_testing_data.

Nachdem das immer noch relativ eintoenig ist, habe ich dir schon eine Menge Repositories herausgesucht, von denen ich weiss, dass sie odML und NIX dateien enthalten. Auch hier sind die Daten wie oben (und in den READMEs in msonntag/metadata-collection) beschrieben aufzunehmen und die Dateien zu sammeln.

odml files:
- https://gin.g-node.org/doi/efish_locking
- https://gin.g-node.org/doi/multielectrode_grasp

NIX files:
- https://gin.g-node.org/doi/Drivers_attention_and_sleep_deprivation

Hier Beispiele fuer ein nicht-DOI repository mit NIX files:
- https://gin.g-node.org/jgrewe/grewe_etal_synchrony

Hier auch das zip file durchsuchen
- https://gin.g-node.org/doi/Henninger2017_electrosensory

Darueber hinaus muessen alle gesammelten odML Files in odML format version 1.1 umgewandelt (odml script odmlconvert der core library) und im Ordner processed/odml-1-1 abgelegt werden, wenn das Original in odML Format version 1 gespeichert war.

Alle NIX files muessen geoeffnet und eventuell enthaltenes odml mit dem nix-odml-converter in einer odML Datei mit dem selben Dateinamen in processed/v1.1 gespeichert werden.

Hier kommt der Teil der von einer programmatischen Seite interessant sein sollte. Der nix-odml-converter ist eine Beta-Version. D.h. er enthaelt noch einiges an Bugs und es gibt sicher einiges, das noch verbessert werden kann. Mach zuerst einmal die nix-odml-converter Issues #22 und #24, da solltest du dann auch schon mit den internals des converters konfrontiert werden.

Wenn du beim Benutzen des nix-odml-converters Bugs entdeckst, mach direkt einen Issue auf und versuche den Bug direkt zu beheben. Wenn dir etwas auffaellt, wie man den converter einfacher oder besser benutzbar zu machen, eroeffne einen Issue, dann koennen Jan, Achilleas und ich mitdiskutieren wie wir den Issue am besten loesen wollen.

Bei den ersten Nix files aus denen du odML extrahierst, vergleiche bitte den tatsaechlichen Inhalt des Nix files mit dem odml das extrahiert wurde daraufhin, ob die Extraktion auch wirklich korrekt funktioniert hat. Falls nicht, mach einen Issue auf, versuch das Problem zu fixen und schreibe gleich einen entsprechenden Test dazu.

Wenn im Laufe des Projekts irgendwas unklar sein sollte oder etwas unerwartetes auftreten soll, melde dich bitte einfach gleich. Wie du dir die Arbeit zwischen durchsuchen, dokumentieren, konvertieren und programmieren im Detail aufteilst, bleibt dir ueberlassen, es sollte nur alles einigermassen regelmaessig passieren d.h. nicht zuerst alles was mit programmieren zu tun hat auf einmal erledigen und die Suche fuer spaeter aufheben.

Das waren jetzt viele Infos auf einmal und das Projekt ist auch auf der einen Seite etwas muehsam, aber doch auch komplex, weil es eine gute Routine abverlangt und viele unterschiedliche Aspekte beachtet werden muessen. Wenn dir also etwas unklar ist und im Detail besprechen moechtest, gib Bescheid, dann koennen wir diese oder kommende Woche gerne eine Videokonferenz ausmachen. Auch wenn du Vorschlaege hast, wie du das Ganze anders angehen moechtest, immer her damit!

Wenn du die Suche und den download ueber ein Script automatisieren moechtest, dann schreibe bitte gleich auch die Informationen die ueber das Readme zu sammeln sind automatisiert in entweder ein gemeinsames JSON oder YAML file und notiere bitte auch, ob ein Repo zip oder tar Dateien enthaelt, falls wir die zu einem spaeteren Zeitpunkt auch durchsuchen moechten.

