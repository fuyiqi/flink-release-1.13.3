################################################################################
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
# limitations under the License.
################################################################################
import logging
import sys

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import (DataTypes, StreamTableEnvironment)
from pyflink.table.udf import udf


def mixing_use_of_datastream_and_table():
    # use StreamTableEnvironment instead of TableEnvironment when mixing use of table & datastream
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)

    # define the source with watermark definition
    t_env.execute_sql("""
            CREATE TABLE source (
                id BIGINT,
                data STRING
            ) with (
                'connector' = 'datagen',
                'number-of-rows' = '10'
            )
        """)

    # define the sink
    t_env.execute_sql("""
            CREATE TABLE sink (
                a BIGINT
            ) with (
                'connector' = 'print'
            )
        """)

    @udf(result_type=DataTypes.BIGINT())
    def length(data):
        return len(data)

    # perform table api operations
    table = t_env.from_path("source")
    table = table.select(table.id, length(table.data))

    # convert table to datastream and perform datastream api operations
    ds = t_env.to_append_stream(table, Types.ROW([Types.LONG(), Types.LONG()]))
    ds = ds.map(lambda i: i[0] + i[1], output_type=Types.LONG())

    # convert datastream to table and perform table api operations as you want
    table = t_env.from_data_stream(ds, 'f0')

    # execute
    table.execute_insert('sink') \
         .wait()
    # remove .wait if submitting to a remote cluster, refer to
    # https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/python/faq/#wait-for-jobs-to-finish-when-executing-jobs-in-mini-cluster
    # for more details


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    mixing_use_of_datastream_and_table()
