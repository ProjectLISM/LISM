#!/bin/bash
# LISM Implementation

declare -i  var
var=1
declare -i i
i=1
echo "`/usr/local/hadoop/bin/hadoop dfsadmin -safemode leave`"
echo "`/usr/local/hadoop/bin/hadoop fs -rmr /home/user/LISM`"
echo "`/usr/local/hadoop/bin/hadoop dfs -copyFromLocal /home/shreemay/LISM/Input/input /home/user/LISM/Input/input.txt`"
echo "Input files copied to hadoop"
echo "Single - "
echo "`/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -mapper /home/shreemay/LISM/single_mapper.py -reducer /home/shreemay/LISM/single_reducer.py -input /home/user/LISM/Input/* -output /home/user/LISM/Single -file /home/shreemay/LISM/config.ini`"
echo "Consistency - "
echo "`/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -mapper /home/shreemay/ASCI/pair_mapper.py -reducer /home/shreemay/LISM/pair_reducer.py -input /home/user/LISM/Input/* -output /home/user/LISM/Consistency -file /home/shreemay/LISM/config.ini`"
echo "Discovery stage - "
echo "Building graph - "
echo "`/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -mapper /home/shreemay/LISM/graph_mapper.py -reducer /home/shreemay/LISM/graph_reducer.py -input /home/user/LISM/Consistency -output /home/user/LISM/Discovery/Graph -file /home/shreemay/LISM/config.ini`"
echo "Generating clique - "
echo "`/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -mapper /home/shreemay/LISM/clique_mapper.py -reducer /home/shreemay/LISM/clique_reducer.py -input /home/user/LISM/Discovery/Graph -output /home/user/LISM/Discovery/Clique/Iter1 -file /home/shreemay/LISM/config.ini`"
file1=$(/usr/local/hadoop/bin/hadoop fs -count [-q] [-h] "/home/user/LISM/Discovery/Graph/part-00000")
filesize1=`echo $file1 | cut -d ' ' -f 3`
file2=$(/usr/local/hadoop/bin/hadoop fs -count [-q] [-h] "/home/user/LISM/Discovery/Graph/part-00000")
filesize2=`echo $file2 | cut -d ' ' -f 3`
while [ $i -gt 0 ];
do 
   string="/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -mapper /home/shreemay/LISM/clique_mapper.py -reducer /home/shreemay/LISM/clique_reducer.py -input /home/user/LISM/Discovery/Clique/Iter"
   string1="$i"
   string2=" -output /home/user/LISM/Discovery/Clique/Iter"
   ((i++))
   string3="$i"
   string4=" -file /home/shreemay/LISM/config.ini"
   echo "`$string$string1$string2$string3$string4`"
   filesize1=$filesize2
   string1="/home/user/LISM/Discovery/Clique/Iter"
   string2="/part-00000"
   file2=$(/usr/local/hadoop/bin/hadoop fs -count [-q] [-h] "$string1$i$string2")
   filesize2=`echo $file2 | cut -d ' ' -f 3`
   if [ $filesize1 -eq $filesize2 ]
   then
      echo "`sudo rm /home/shreemay/LISM/clique`"
      echo "`/usr/local/hadoop/bin/hadoop dfs -copyToLocal /home/user/LISM/Discovery/Clique/Iter$i/part-00000 /home/shreemay/LISM/clique`"
      break
   fi
done
string1="/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -mapper /home/shreemay/LISM/bridge_mapper.py -reducer /home/shreemay/LISM/bridge_reducer.py -input /home/user/LISM/Discovery/Clique/Iter"
string2=" -output /home/user/LISM/Discovery/Bridge -file /home/shreemay/LISM/config.ini"
echo "`$string1$i$string2`"
echo "`python indexing.py /home/shreemay/LISM/clique`"
echo "`sudo rm /home/shreemay/LISM/bridge`"
echo "`/usr/local/hadoop/bin/hadoop dfs -copyToLocal /home/user/LISM/Discovery/Bridge/part-00000 /home/shreemay/LISM/bridge`"
echo "`python bridge_store.py`"
