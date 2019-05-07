https://packaging.python.org/guides/analyzing-pypi-package-downloads/#useful-queries

https://bigquery.cloud.google.com/table/the-psf:pypi.downloads?pli=1

https://bigquery.cloud.google.com/results/jovial-opus-208514:US.bquijob_4330630b_1646a36b96e

# odml

SELECT country_code, timestamp, file.filename, details.installer.name, details.installer.version, details.python, details.system.name
FROM TABLE_DATE_RANGE(
  [the-psf:pypi.downloads],
  TIMESTAMP("2018-05-01"),
  CURRENT_TIMESTAMP()
)
WHERE file.project="odml" and details.installer.name="pip"

2018-05 - 2018-06

{"country_code":"US","timestamp":"1.526268465E9","file_filename":"odML-1.3.4.1.tar.gz","details_installer_name":"pip","details_installer_version":"10.0.1","details_python":"2.7.15rc1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.526290494E9","file_filename":"odML-1.3.4.1.tar.gz","details_installer_name":"pip","details_installer_version":"10.0.1","details_python":"2.7.15rc1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.527251314E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.3","details_python":"3.5.1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.527063137E9","file_filename":"odML-1.3.4.1.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.3","details_python":"3.5.1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.527588424E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.3","details_python":"3.5.1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.527068069E9","file_filename":"odML-1.3.4.1.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.3","details_python":"3.5.1","details_system_name":"Linux"}
{"country_code":"CZ","timestamp":"1.527672676E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"10.0.1","details_python":"3.5.2","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.527667524E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.3","details_python":"3.5.1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.527667563E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.3","details_python":"3.5.1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.527596167E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.3","details_python":"3.5.1","details_system_name":"Linux"}
{"country_code":"US","timestamp":"1.529743741E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"10.0.1","details_python":"2.7.12","details_system_name":"Linux"}
{"country_code":null,"timestamp":"1.529407578E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.1","details_python":"2.7.15rc1","details_system_name":"Linux"}
{"country_code":"DE","timestamp":"1.530789753E9","file_filename":"odML-1.4.0.3.tar.gz","details_installer_name":"pip","details_installer_version":"9.0.1","details_python":"2.7.15rc1","details_system_name":"Linux"}

# nixio

SELECT country_code, timestamp, file.filename, details.installer.name, details.installer.version, details.python, details.system.name
FROM TABLE_DATE_RANGE(
  [the-psf:pypi.downloads],
  TIMESTAMP("2018-05-01"),
  CURRENT_TIMESTAMP()
)
WHERE file.project="nixio" and details.installer.name="pip"

2018-05 - 2018-06

country_code	timestamp	file_filename	details_installer_name	details_installer_version	details_python	details_system_name
	2018-05-09 06:55:56 UTC	nixio-1.4.4-py3-none-any.whl	pip	10.0.1	3.6.5	Linux
US	2018-05-07 23:34:35 UTC	nixio-1.4.4-py3-none-any.whl	pip	9.0.1	3.6.4	Windows
US	2018-05-18 08:41:32 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
US	2018-05-18 08:41:29 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
US	2018-05-13 23:18:00 UTC	nixio-1.4.4-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
US	2018-05-13 23:17:53 UTC	nixio-1.4.4-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
US	2018-05-23 14:51:01 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
DE	2018-05-25 12:46:52 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.5.3	Linux
DE	2018-05-25 12:46:45 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.6.5	Linux
US	2018-05-23 13:49:58 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
US	2018-05-24 14:17:24 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
IN	2018-05-27 15:41:47 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.6.4	Windows
ES	2018-05-25 09:53:05 UTC	nixio-1.4.5-py2-none-any.whl	pip	9.0.1	2.7.14	Windows
	2018-05-27 17:51:30 UTC	nixio-1.4.5-py2-none-any.whl	pip	9.0.1	2.7.14	Linux
US	2018-06-03 07:57:55 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-03 08:02:10 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-03 08:01:17 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.4	Windows
US	2018-06-06 19:37:34 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-07 00:24:27 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-03 10:06:28 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.4	Windows
US	2018-06-03 10:02:09 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-21 13:58:08 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
RU	2018-06-06 13:02:17 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.12	Linux
US	2018-06-03 06:08:01 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-03 06:11:39 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.4	Windows
US	2018-06-04 23:11:09 UTC	nixio-1.3.1-py3-none-any.whl	pip	10.0.1	3.5.2	Linux
US	2018-06-05 18:45:09 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.4	Windows
US	2018-06-08 10:17:18 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
DE	2018-06-12 15:49:51 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.5.2	Linux
US	2018-06-08 01:48:59 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.4	Windows
US	2018-06-08 01:44:14 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.4	Windows
US	2018-06-15 20:28:12 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-14 18:41:31 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-13 20:57:40 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.4	Windows
US	2018-06-13 20:53:21 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
CN	2018-06-09 17:30:57 UTC	nixio-1.4.5-py3-none-any.whl	pip	8.1.1	3.5.2	Linux
US	2018-06-20 12:45:11 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
ES	2018-06-21 15:43:12 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-22 09:11:37 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
US	2018-06-15 19:40:50 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-06-15 19:45:43 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Windows
US	2018-07-02 11:50:05 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
ES	2018-06-21 11:19:23 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.4	Windows
IN	2018-06-15 04:34:31 UTC	nixio-1.4.5-py2-none-any.whl	pip	8.1.1	2.7.12	Linux
US	2018-06-29 07:12:24 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
US	2018-07-02 12:51:39 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.1	3.6.1	Linux
US	2018-07-02 12:51:55 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
US	2018-06-27 07:12:32 UTC	nixio-1.4.5-py2-none-any.whl	pip	10.0.1	2.7.15	Linux
GR	2018-07-04 08:51:51 UTC	nixio-1.4.5-py2-none-any.whl	pip	9.0.3	2.7.9	Linux
IN	2018-06-10 12:25:09 UTC	nixio-1.4.5-py3-none-any.whl	pip	9.0.3	3.6.5	Windows
US	2018-07-02 22:20:18 UTC	nixio-1.4.5-py3-none-any.whl	pip	10.0.1	3.4.2	Linux
