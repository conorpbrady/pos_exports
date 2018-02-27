
from lib.infogenesisdatabase import InfogenesisDatabase
ig_db = InfogenesisDatabase()
ig_db.init_queries()
ig_db.create_tables()
ig_db.insert_values()
ig_db.close()
