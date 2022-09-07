Storing logs in MyRocks. More than a billion rows. LZ4 compression.

```
apt-get install mariadb-plugin-rocksdb
```

Config `/etc/mysql/mariadb.conf.d/rocksdb.cnf`

```
[mariadb]
plugin-load-add=ha_rocksdb.so
rocksdb_db_write_buffer_size = 128M
rocksdb_flush_log_at_trx_commit = 2
rocksdb_max_background_jobs = 4
rocksdb_block_cache_size = 1G
rocksdb_block_size = 16K
rocksdb-override-cf-options='default={target_file_size_base=32m;block_based_table_factory={filter_policy=bloomfilter:10:false;whole_key_filtering=1};compression=kNoCompression;bottommost_compression=kLZ4Compression;level_compaction_dynamic_level_bytes=true;compaction_pri=kMinOverlappingRatio;}'
```

Create table.
```
CREATE TABLE `logs` (
  `date` date NOT NULL DEFAULT current_timestamp(),
  `rid` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `mes` blob NOT NULL
) ENGINE=ROCKSDB DEFAULT CHARSET=binary;
```

Create index.
```
ALTER TABLE `logs`
  ADD KEY `a` (`rid`,`date`);
COMMIT;
```

Try query.
```
MariaDB [db]> SELECT `time`, `mes` FROM `logs` WHERE `rid` = 27842 AND `date` = current_date ORDER BY `time` DESC;
...
1843 rows in set (0.012 sec)
```

```
MariaDB [db]> DESCRIBE SELECT `time`, `mes` FROM `logs` WHERE `rid` = 27842 AND `date` = current_date ORDER BY `time` DESC;
+------+-------------+-------+------+---------------+------+---------+-------------+------+----------------------------------------------------+
| id   | select_type | table | type | possible_keys | key  | key_len | ref         | rows | Extra                                              |
+------+-------------+-------+------+---------------+------+---------+-------------+------+----------------------------------------------------+
|    1 | SIMPLE      | logs  | ref  | a             | a    | 7       | const,const | 2222 | Using index condition; Using where; Using filesort |
+------+-------------+-------+------+---------------+------+---------+-------------+------+----------------------------------------------------+
```

Logs example.
```
[14:42:18] h
[14:42:18] a["{\"args\":[\"324\"],\"callback\":null,\"method\":\"onRoomCountUpdate\"}"]
[14:42:14] a["{\"args\":[\"{\\\"type\\\": \\\"appnotice\\\", \\\"msg\\\": [\\\"%%%[emoticon StunningGirl|https://static-pub.highwebmedia.com/uploads/avatar/2015/05/20/00/16/b3548f0aa7e0382723513bc427b696ac66cb2f4f.jpg|250|80|/emoticon_report_abuse/StunningGirl/]%%%\\\"], \\\"background\\\": \\\"linear-gradient(to right,rgba(0,191,255,0.0) 4.0%,rgba(0,191,255,0.1) 13.0%,rgba(0,191,255,0.2) 33.0%,rgba(0,191,255,0.2) 60.0%,rgba(255,212,38,0.2) 100.0%,rgba(255,212,38,0.3) 100.0%)\\\", \\\"foreground\\\": \\\"rgb(0,0,0)\\\", \\\"weight\\\": \\\"bold\\\", \\\"tid\\\": \\\"16625617345:19216\\\"}\"],\"callback\":null,\"method\":\"onNotify\"}"]
[14:42:11] a["{\"args\":[\"{\\\"type\\\": \\\"appnotice\\\", \\\"msg\\\": [\\\"%%%[emoticon babyboard4|https://static-pub.highwebmedia.com/uploads/avatar/2021/04/12/07/37/b5a39f36693998e764497704b2cab18285efbb85.jpg|141|26|/emoticon_report_abuse/babyboard4/]%%%\\\", \\\"%%%[emoticon bblev1|https://static-pub.highwebmedia.com/uploads/avatar/2017/01/28/07/52/afae4793b0cf8a02830a736176bf162f6bd971bd.jpg|15|15|/emoticon_report_abuse/bblev1/]%%% %%%[emoticon minipixelcrown_2|https://static-pub.highwebmedia.com/uploads/avatar/2017/05/03/11/47/1417b0c6a609d9f3ec08f055eab75ad38006736e.jpg|25|18|/emoticon_report_abuse/minipixelcrown_2/]%%% jefo42069 |777|\\\", \\\"%%%[emoticon bblev2|https://static-pub.highwebmedia.com/uploads/avatar/2017/01/28/07/52/210c6b4069f60a261ab01c05aa9697b428bfbb45.jpg|15|15|/emoticon_report_abuse/bblev2/]%%% cocacolarabbit31 |1|\\\", \\\"%%%[emoticon bblev3|https://static-pub.highwebmedia.com/uploads/avatar/2017/01/28/07/52/10365d793ba306a2b60329266de26ab3478ed45f.jpg|15|15|/emoticon_report_abuse/bblev3/]%%% sexybanker_989 |1|\\\"], \\\"weight\\\": \\\"bold\\\", \\\"tid\\\": \\\"16625617315:39229\\\"}\"],\"callback\":null,\"method\":\"onNotify\"}"]
[14:41:53] h
```

Table size.

<img src="https://img.poiuty.com/a/3b/45e9617da6e59a285d331ebccef5343b.jpg">


https://mariadb.com/kb/en/getting-started-with-myrocks/<br/>
https://github.com/facebook/rocksdb/wiki/Space-Tuning<br/>
https://github.com/facebook/rocksdb/wiki/Compression<br/>
https://raw.githubusercontent.com/facebook/zstd/dev/doc/images/CSpeed2.png<br/>
https://mariadb.com/kb/en/getting-started-with-myrocks/+comments/3412<br/>
https://dataops.barcelona/wp-content/uploads/2019/07/MyRocks-101.pdf<br/>
https://rocksdb.org/blog/2015/07/23/dynamic-level.html<br/>
