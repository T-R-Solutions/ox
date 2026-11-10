"""Age checks against real public diagnostics and rejected successor metadata."""
import datetime,json,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class DatabaseAge(unittest.TestCase):
 def accepted(self, record, scanner):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/'record.json';path.write_text(json.dumps(record))
   run=subprocess.run(['bash','-c','source "$1"; validate_database_age "$2" "$3"','age',str(ROOT/'scripts/lib/backends.sh'),str(path),scanner],capture_output=True)
   return run.returncode==0
 def record(self,age):
  timestamp=(datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=age)).isoformat()
  return {'database':'a'*64,'database_metadata':{'schema':1,'snapshot':'a'*64,'data_timestamp':timestamp,'timestamp_semantics':'oldest_required_source','sources':[{'url':'https://official.example','sha256':'b'*64,'data_timestamp':timestamp,'timestamp_semantics':'native_database_updated_at'}]*2}}
 def test_age_boundaries_and_inconsistent_identity(self):
  for scanner,limit in [('osv',24),('trivy',120)]:
   self.assertTrue(self.accepted(self.record(limit-1),scanner))
   for age in [limit+1,-1]: self.assertFalse(self.accepted(self.record(age),scanner))
   record=self.record(1);record['database_metadata']['snapshot']='b'*64
   self.assertFalse(self.accepted(record,scanner))
   record=self.record(1);record['database_metadata']['data_timestamp']='2000-01-01T00:00:00Z'
   self.assertFalse(self.accepted(record,scanner))
   record=self.record(1);del record['database_metadata']['sources'][0]['data_timestamp']
   self.assertFalse(self.accepted(record,scanner))
