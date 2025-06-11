# SPDX-FileCopyrightText: 2023-2025 The ReReSo Authors, see AUTHORS.md
#
# SPDX-License-Identifier: Apache-2.0

.NOTINTERMEDIATE:
.PHONY: all clean

ABBADINGO_ONE_NAMES = 1 2 3 4 5 6 7 8 9 a b c d r s t
ABBADINGO_ONE_DATA = $(foreach name,$(ABBADINGO_ONE_NAMES),abbadingo-one/train.$(name).gz)
ABBADINGO_ONE_BENCHMARKS = $(foreach name,$(ABBADINGO_ONE_NAMES),abbadingo-one/abbadingo-one-$(name).json.zst)

DISC_IDS = 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
DISC_ALFRED_BENCHMARKS = $(foreach id,$(DISC_IDS),disc/disc-alfred-$(id).json.zst)
DISC_MALWARE_BATTERY_LOW_BENCHMARKS = $(foreach id,$(DISC_IDS),disc/disc-malware-BATTERY_LOW-$(id).json.zst)
DISC_MALWARE_BOOT_COMPLETED_BENCHMARKS = $(foreach id,$(DISC_IDS),disc/disc-malware-BOOT_COMPLETED-$(id).json.zst)
DISC_MIT_AR_BENCHMARKS = $(foreach id,$(DISC_IDS),disc/disc-mit_1-$(id).json.zst)

HADOOP_APPLICATIONS = PageRank WordCount
HADOOP_BENCHMARKS = $(foreach app,$(HADOOP_APPLICATIONS),hadoop/hadoop-$(app).json.zst)

all: $(ABBADINGO_ONE_BENCHMARKS) \
     alfred/alfred.json.zst \
     $(DISC_ALFRED_BENCHMARKS) $(DISC_MALWARE_BATTERY_LOW_BENCHMARKS) \
     $(DISC_MALWARE_BOOT_COMPLETED_BENCHMARKS) $(DISC_MIT_AR_BENCHMARKS) \
     $(HADOOP_BENCHMARKS) \
     mit-ar/mit-ar.json.zst

clean:
	rm -rf rereso-0.3.1 rereso-0.3.1.zip \
           $(ABBADINGO_ONE_BENCHMARKS) $(ABBADINGO_ONE_DATA) \
           alfred/alfred.json.zst alfred/json_2.1.0.7z \
           $(DISC_ALFRED_BENCHMARKS) $(DISC_MALWARE_BATTERY_LOW_BENCHMARKS) \
           $(DISC_MALWARE_BOOT_COMPLETED_BENCHMARKS) $(DISC_MIT_AR_BENCHMARKS) \
           disc/DISC-master disc/DISC-master.zip \
           $(HADOOP_BENCHMARKS) hadoop/LogHub-Hadoop.zip hadoop/LogHub-2.0-Hadoop.zip \
           mit-ar/mit-ar.json.zst mit-ar/thesis_data_matlab.zip

rereso-0.3.1: | rereso-0.3.1.zip
	rm -rf $@
	unzip -qq rereso-0.3.1.zip

rereso-0.3.1.zip:
	wget -q --continue \
         https://github.com/tudo-aqua/rereso/releases/download/$(@:rereso-%.zip=%)/$@

abbadingo-one/abbadingo-one-%.json.zst: abbadingo-one/train.%.gz rereso-0.3.1
	$(word 2,$^)/bin/rereso abbadingo-one $< $@

abbadingo-one/train.%.gz:
	cd abbadingo-one; wget -q --continue \
                           https://abbadingo.cs.nuim.ie/data-sets/$(@:abbadingo-one/%=%)

alfred/alfred.json.zst: alfred/json_2.1.0.7z rereso-0.3.1
	$(word 2,$^)/bin/rereso alfred $< $@

alfred/json_2.1.0.7z:
	cd alfred; wget -q --continue \
                    https://ai2-vision-alfred.s3-us-west-2.amazonaws.com/$(@:alfred/%=%)

$(DISC_ALFRED_BENCHMARKS)&: disc/DISC-master rereso-0.3.1
	$(word 2,$^)/bin/rereso disc-all $</traces/alfred disc -t disc-alfred-\<id\>.json.zst

$(DISC_MALWARE_BATTERY_LOW_BENCHMARKS)&: disc/DISC-master rereso-0.3.1
	$(word 2,$^)/bin/rereso disc-all $</traces/malware/BATTERY_LOW disc -t disc-malware-BATTERY_LOW-\<id\>.json.zst

$(DISC_MALWARE_BOOT_COMPLETED_BENCHMARKS)&: disc/DISC-master rereso-0.3.1
	$(word 2,$^)/bin/rereso disc-all $</traces/malware/BOOT_COMPLETED disc -t disc-malware-BOOT_COMPLETED-\<id\>.json.zst

$(DISC_MIT_AR_BENCHMARKS)&: disc/DISC-master rereso-0.3.1
	$(word 2,$^)/bin/rereso disc-all $</traces/mit_1 disc -t disc-mit_1-\<id\>.json.zst

disc/DISC-master: | disc/DISC-master.zip
	rm -rf $@
	cd disc; unzip -qq DISC-master.zip

disc/DISC-master.zip:
	cd disc; wget -q --continue --trust-server-names --content-disposition \
                  https://github.com/andrewli77/DISC/archive/refs/heads/master.zip

$(HADOOP_BENCHMARKS)&: hadoop/LogHub-Hadoop.zip hadoop/LogHub-2.0-Hadoop.zip rereso-0.3.1
	$(word 3,$^)/bin/rereso hadoop-loghub $< $(word 2,$^) hadoop -t hadoop-\<id\>.json.zst

hadoop/LogHub-Hadoop.zip:
	wget -q --continue https://zenodo.org/records/8196385/files/Hadoop.zip -O $@

hadoop/LogHub-2.0-Hadoop.zip:
	wget -q --continue https://zenodo.org/records/8275861/files/Hadoop.zip -O $@

mit-ar/mit-ar.json.zst: mit-ar/thesis_data_matlab.zip rereso-0.3.1
	$(word 2,$^)/bin/rereso mit-ar $< $@

mit-ar/thesis_data_matlab.zip:
	cd mit-ar; wget -q --continue \
                    https://courses.media.mit.edu/2004fall/mas622j/04.projects/home/$(@:mit-ar/%=%)
