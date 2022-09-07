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

<img src="https://img.poiuty.com/a/3b/45e9617da6e59a285d331ebccef5343b.jpg">


https://mariadb.com/kb/en/getting-started-with-myrocks/<br/>
https://github.com/facebook/rocksdb/wiki/Space-Tuning<br/>
https://github.com/facebook/rocksdb/wiki/Compression<br/>
https://raw.githubusercontent.com/facebook/zstd/dev/doc/images/CSpeed2.png<br/>
https://mariadb.com/kb/en/getting-started-with-myrocks/+comments/3412<br/>
https://dataops.barcelona/wp-content/uploads/2019/07/MyRocks-101.pdf<br/>
https://rocksdb.org/blog/2015/07/23/dynamic-level.html<br/>
