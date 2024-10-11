{
    "ok" : 1.0,
    "capped" : false,
    "wiredTiger" : {
        "metadata" : {
            "formatVersion" : 1.0
        },
        "creationString" : "access_pattern_hint=none,allocation_size=4KB,app_metadata=(formatVersion=1),assert=(commit_timestamp=none,durable_timestamp=none,read_timestamp=none,write_timestamp=off),block_allocation=best,block_compressor=snappy,cache_resident=false,checksum=on,colgroups=,collator=,columns=,dictionary=0,encryption=(keyid=,name=),exclusive=false,extractor=,format=btree,huffman_key=,huffman_value=,ignore_in_memory_cache_size=false,immutable=false,import=(enabled=false,file_metadata=,repair=false),internal_item_max=0,internal_key_max=0,internal_key_truncate=true,internal_page_max=32KB,key_format=q,key_gap=10,leaf_item_max=0,leaf_key_max=0,leaf_page_max=128KB,leaf_value_max=64MB,log=(enabled=true),lsm=(auto_throttle=true,bloom=true,bloom_bit_count=16,bloom_config=,bloom_hash_count=8,bloom_oldest=false,chunk_count_limit=0,chunk_max=5GB,chunk_size=10MB,merge_custom=(prefix=,start_generation=0,suffix=),merge_max=15,merge_min=0),memory_page_image_max=0,memory_page_max=10m,os_cache_dirty_max=0,os_cache_max=0,prefix_compression=false,prefix_compression_min=4,readonly=false,source=,split_deepen_min_child=0,split_deepen_per_child=0,split_pct=90,tiered_object=false,tiered_storage=(auth_token=,bucket=,bucket_prefix=,local_retention=300,name=,object_target_size=10M),type=file,value_format=u,verbose=[],write_timestamp_usage=none",
        "type" : "file",
        "uri" : "statistics:table:collection-20--4865285679507410014",
        "LSM" : {
            "bloom filter false positives" : 0.0,
            "bloom filter hits" : 0.0,
            "bloom filter misses" : 0.0,
            "bloom filter pages evicted from cache" : 0.0,
            "bloom filter pages read into cache" : 0.0,
            "bloom filters in the LSM tree" : 0.0,
            "chunks in the LSM tree" : 0.0,
            "highest merge generation in the LSM tree" : 0.0,
            "queries that could have benefited from a Bloom filter that did not exist" : 0.0,
            "sleep for LSM checkpoint throttle" : 0.0,
            "sleep for LSM merge throttle" : 0.0,
            "total size of bloom filters" : 0.0
        },
        "block-manager" : {
            "allocations requiring file extension" : 0.0,
            "blocks allocated" : 0.0,
            "blocks freed" : 0.0,
            "checkpoint size" : 0.0,
            "file allocation unit size" : 4096.0,
            "file bytes available for reuse" : 0.0,
            "file magic number" : 120897.0,
            "file major version number" : 1.0,
            "file size in bytes" : 4096.0,
            "minor version number" : 0.0
        },
        "btree" : {
            "btree checkpoint generation" : 3294.0,
            "btree clean tree checkpoint expiration time" : 9223372036854775807,
            "column-store fixed-size leaf pages" : 0.0,
            "column-store internal pages" : 0.0,
            "column-store variable-size RLE encoded values" : 0.0,
            "column-store variable-size deleted values" : 0.0,
            "column-store variable-size leaf pages" : 0.0,
            "fixed-record size" : 0.0,
            "maximum internal page key size" : 2867.0,
            "maximum internal page size" : 32768.0,
            "maximum leaf page key size" : 11878.0,
            "maximum leaf page size" : 131072.0,
            "maximum leaf page value size" : 67108864.0,
            "maximum tree depth" : 0.0,
            "number of key/value pairs" : 0.0,
            "overflow pages" : 0.0,
            "pages rewritten by compaction" : 0.0,
            "row-store empty values" : 0.0,
            "row-store internal pages" : 0.0,
            "row-store leaf pages" : 0.0
        },
        "cache" : {
            "bytes currently in the cache" : 182.0,
            "bytes dirty in the cache cumulative" : 0.0,
            "bytes read into cache" : 0.0,
            "bytes written from cache" : 0.0,
            "checkpoint blocked page eviction" : 0.0,
            "checkpoint of history store file blocked non-history store page eviction" : 0.0,
            "data source pages selected for eviction unable to be evicted" : 0.0,
            "eviction gave up due to detecting an out of order on disk value behind the last update on the chain" : 0.0,
            "eviction gave up due to detecting an out of order tombstone ahead of the selected on disk update" : 0.0,
            "eviction gave up due to detecting an out of order tombstone ahead of the selected on disk update after validating the update chain" : 0.0,
            "eviction gave up due to detecting out of order timestamps on the update chain after the selected on disk update" : 0.0,
            "eviction walk passes of a file" : 0.0,
            "eviction walk target pages histogram - 0-9" : 0.0,
            "eviction walk target pages histogram - 10-31" : 0.0,
            "eviction walk target pages histogram - 128 and higher" : 0.0,
            "eviction walk target pages histogram - 32-63" : 0.0,
            "eviction walk target pages histogram - 64-128" : 0.0,
            "eviction walk target pages reduced due to history store cache pressure" : 0.0,
            "eviction walks abandoned" : 0.0,
            "eviction walks gave up because they restarted their walk twice" : 0.0,
            "eviction walks gave up because they saw too many pages and found no candidates" : 0.0,
            "eviction walks gave up because they saw too many pages and found too few candidates" : 0.0,
            "eviction walks reached end of tree" : 0.0,
            "eviction walks restarted" : 0.0,
            "eviction walks started from root of tree" : 0.0,
            "eviction walks started from saved location in tree" : 0.0,
            "hazard pointer blocked page eviction" : 0.0,
            "history store table insert calls" : 0.0,
            "history store table insert calls that returned restart" : 0.0,
            "history store table out-of-order resolved updates that lose their durable timestamp" : 0.0,
            "history store table out-of-order updates that were fixed up by reinserting with the fixed timestamp" : 0.0,
            "history store table reads" : 0.0,
            "history store table reads missed" : 0.0,
            "history store table reads requiring squashed modifies" : 0.0,
            "history store table truncation by rollback to stable to remove an unstable update" : 0.0,
            "history store table truncation by rollback to stable to remove an update" : 0.0,
            "history store table truncation to remove an update" : 0.0,
            "history store table truncation to remove range of updates due to key being removed from the data page during reconciliation" : 0.0,
            "history store table truncation to remove range of updates due to out-of-order timestamp update on data page" : 0.0,
            "history store table writes requiring squashed modifies" : 0.0,
            "in-memory page passed criteria to be split" : 0.0,
            "in-memory page splits" : 0.0,
            "internal pages evicted" : 0.0,
            "internal pages split during eviction" : 0.0,
            "leaf pages split during eviction" : 0.0,
            "modified pages evicted" : 0.0,
            "overflow pages read into cache" : 0.0,
            "page split during eviction deepened the tree" : 0.0,
            "page written requiring history store records" : 0.0,
            "pages read into cache" : 0.0,
            "pages read into cache after truncate" : 0.0,
            "pages read into cache after truncate in prepare state" : 0.0,
            "pages requested from the cache" : 0.0,
            "pages seen by eviction walk" : 0.0,
            "pages written from cache" : 0.0,
            "pages written requiring in-memory restoration" : 0.0,
            "tracked dirty bytes in the cache" : 0.0,
            "unmodified pages evicted" : 0.0
        },
        "cache_walk" : {
            "Average difference between current eviction generation when the page was last considered" : 0.0,
            "Average on-disk page image size seen" : 0.0,
            "Average time in cache for pages that have been visited by the eviction server" : 0.0,
            "Average time in cache for pages that have not been visited by the eviction server" : 0.0,
            "Clean pages currently in cache" : 0.0,
            "Current eviction generation" : 0.0,
            "Dirty pages currently in cache" : 0.0,
            "Entries in the root page" : 0.0,
            "Internal pages currently in cache" : 0.0,
            "Leaf pages currently in cache" : 0.0,
            "Maximum difference between current eviction generation when the page was last considered" : 0.0,
            "Maximum page size seen" : 0.0,
            "Minimum on-disk page image size seen" : 0.0,
            "Number of pages never visited by eviction server" : 0.0,
            "On-disk page image sizes smaller than a single allocation unit" : 0.0,
            "Pages created in memory and never written" : 0.0,
            "Pages currently queued for eviction" : 0.0,
            "Pages that could not be queued for eviction" : 0.0,
            "Refs skipped during cache traversal" : 0.0,
            "Size of the root page" : 0.0,
            "Total number of pages currently in cache" : 0.0
        },
        "checkpoint-cleanup" : {
            "pages added for eviction" : 0.0,
            "pages removed" : 0.0,
            "pages skipped during tree walk" : 0.0,
            "pages visited" : 0.0
        },
        "compression" : {
            "compressed page maximum internal page size prior to compression" : 524288.0,
            "compressed page maximum leaf page size prior to compression " : 524288.0,
            "compressed pages read" : 0.0,
            "compressed pages written" : 0.0,
            "page written failed to compress" : 0.0,
            "page written was too small to compress" : 0.0
        },
        "cursor" : {
            "Total number of entries skipped by cursor next calls" : 0.0,
            "Total number of entries skipped by cursor prev calls" : 0.0,
            "Total number of entries skipped to position the history store cursor" : 0.0,
            "Total number of pages skipped without reading by cursor next calls" : 0.0,
            "Total number of pages skipped without reading by cursor prev calls" : 0.0,
            "Total number of times a search near has exited due to prefix config" : 0.0,
            "bulk loaded cursor insert calls" : 0.0,
            "cache cursors reuse count" : 1.0,
            "close calls that result in cache" : 1.0,
            "create calls" : 1.0,
            "cursor next calls that skip due to a globally visible history store tombstone" : 0.0,
            "cursor next calls that skip greater than or equal to 100 entries" : 0.0,
            "cursor next calls that skip less than 100 entries" : 1.0,
            "cursor prev calls that skip due to a globally visible history store tombstone" : 0.0,
            "cursor prev calls that skip greater than or equal to 100 entries" : 0.0,
            "cursor prev calls that skip less than 100 entries" : 0.0,
            "insert calls" : 0.0,
            "insert key and value bytes" : 0.0,
            "modify" : 0.0,
            "modify key and value bytes affected" : 0.0,
            "modify value bytes modified" : 0.0,
            "next calls" : 1.0,
            "open cursor count" : 0.0,
            "operation restarted" : 0.0,
            "prev calls" : 0.0,
            "remove calls" : 0.0,
            "remove key bytes removed" : 0.0,
            "reserve calls" : 0.0,
            "reset calls" : 2.0,
            "search calls" : 0.0,
            "search history store calls" : 0.0,
            "search near calls" : 0.0,
            "truncate calls" : 0.0,
            "update calls" : 0.0,
            "update key and value bytes" : 0.0,
            "update value size change" : 0.0
        },
        "reconciliation" : {
            "approximate byte size of timestamps in pages written" : 0.0,
            "approximate byte size of transaction IDs in pages written" : 0.0,
            "dictionary matches" : 0.0,
            "fast-path pages deleted" : 0.0,
            "internal page key bytes discarded using suffix compression" : 0.0,
            "internal page multi-block writes" : 0.0,
            "internal-page overflow keys" : 0.0,
            "leaf page key bytes discarded using prefix compression" : 0.0,
            "leaf page multi-block writes" : 0.0,
            "leaf-page overflow keys" : 0.0,
            "maximum blocks required for a page" : 0.0,
            "overflow values written" : 0.0,
            "page checksum matches" : 0.0,
            "page reconciliation calls" : 0.0,
            "page reconciliation calls for eviction" : 0.0,
            "pages deleted" : 0.0,
            "pages written including an aggregated newest start durable timestamp " : 0.0,
            "pages written including an aggregated newest stop durable timestamp " : 0.0,
            "pages written including an aggregated newest stop timestamp " : 0.0,
            "pages written including an aggregated newest stop transaction ID" : 0.0,
            "pages written including an aggregated newest transaction ID " : 0.0,
            "pages written including an aggregated oldest start timestamp " : 0.0,
            "pages written including an aggregated prepare" : 0.0,
            "pages written including at least one prepare" : 0.0,
            "pages written including at least one start durable timestamp" : 0.0,
            "pages written including at least one start timestamp" : 0.0,
            "pages written including at least one start transaction ID" : 0.0,
            "pages written including at least one stop durable timestamp" : 0.0,
            "pages written including at least one stop timestamp" : 0.0,
            "pages written including at least one stop transaction ID" : 0.0,
            "records written including a prepare" : 0.0,
            "records written including a start durable timestamp" : 0.0,
            "records written including a start timestamp" : 0.0,
            "records written including a start transaction ID" : 0.0,
            "records written including a stop durable timestamp" : 0.0,
            "records written including a stop timestamp" : 0.0,
            "records written including a stop transaction ID" : 0.0
        },
        "session" : {
            "object compaction" : 0.0,
            "tiered operations dequeued and processed" : 0.0,
            "tiered operations scheduled" : 0.0,
            "tiered storage local retention time (secs)" : 0.0,
            "tiered storage object size" : 0.0
        },
        "transaction" : {
            "race to read prepared update retry" : 0.0,
            "rollback to stable history store records with stop timestamps older than newer records" : 0.0,
            "rollback to stable inconsistent checkpoint" : 0.0,
            "rollback to stable keys removed" : 0.0,
            "rollback to stable keys restored" : 0.0,
            "rollback to stable restored tombstones from history store" : 0.0,
            "rollback to stable restored updates from history store" : 0.0,
            "rollback to stable skipping delete rle" : 0.0,
            "rollback to stable skipping stable rle" : 0.0,
            "rollback to stable sweeping history store keys" : 0.0,
            "rollback to stable updates removed from history store" : 0.0,
            "transaction checkpoints due to obsolete pages" : 0.0,
            "update conflicts" : 0.0
        }
    },
    "sharded" : false,
    "size" : 0.0,
    "count" : 0.0,
    "storageSize" : 4096.0,
    "totalIndexSize" : 4096.0,
    "totalSize" : 8192.0,
    "indexSizes" : {
        "_id_" : 4096.0
    },
    "avgObjSize" : 0.0,
    "ns" : "prod_archive.prod_tagger_archive_jul_w3_new",
    "nindexes" : 1.0,
    "scaleFactor" : 1.0
}
