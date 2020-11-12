from neo4j import GraphDatabase

class Neo4j_Executor:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_query(self, query):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._execute_query, query)
            return greeting

    @staticmethod
    def _execute_query(tx, query):
        result = tx.run(query)
        return [r.values()[0] for r in result]


# if __name__ == "__main__":
#     greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "i110873")
#     greeter.print_greeting("hello, world")
#     greeter.close()


# from neo4j import GraphDatabase
#
# class Neo4j_Executor:
#
#     def __init__(self, uri, user, password):
#         self.driver = GraphDatabase.driver(uri, auth=(user, password))
#
#     def close(self):
#         self.driver.close()
#
#
#     # @staticmethod
#     def execute_query(self, query):
#         tx = self.driver
#         result = tx.run(query)
#         return result.single()[0]
#
#
# # if __name__ == "__main__":
# #     greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "i110873")
# #     greeter.print_greeting("hello, world")
# #     greeter.close()