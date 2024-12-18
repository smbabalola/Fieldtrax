# from typing import Dict, Any, List, Optional
# from datetime import datetime
# import json
# from pathlib import Path
# from sqlalchemy.orm import Session

# # Create base directory for offline storage
# OFFLINE_DB_DIR = Path(__file__).parent.parent / 'offline_db'
# OFFLINE_DB_DIR.mkdir(exist_ok=True)

# class SyncManager:
#     def __init__(self):
#         self.sync_dir = OFFLINE_DB_DIR / 'sync'
#         self.sync_dir.mkdir(exist_ok=True)
#         self.pending_file = self.sync_dir / 'pending_changes.json'
#         self.pending_changes: List[Dict[str, Any]] = []
#         self._load_pending_changes()

#     def _load_pending_changes(self) -> None:
#         """Load pending changes from file"""
#         try:
#             if self.pending_file.exists():
#                 with open(self.pending_file, 'r') as f:
#                     self.pending_changes = json.load(f)
#             else:
#                 self.pending_changes = []
#                 self._save_pending_changes()
#         except Exception as e:
#             print(f"Error loading pending changes: {e}")
#             self.pending_changes = []

#     def _save_pending_changes(self) -> None:
#         """Save pending changes to file"""
#         try:
#             with open(self.pending_file, 'w') as f:
#                 json.dump(self.pending_changes, f)
#         except Exception as e:
#             print(f"Error saving pending changes: {e}")

#     def record_change(
#         self, 
#         table_name: str, 
#         operation: str, 
#         data: Dict[str, Any]
#     ) -> None:
#         """Record a change for later synchronization"""
#         change = {
#             'timestamp': datetime.utcnow().isoformat(),
#             'table': table_name,
#             'operation': operation,
#             'data': data,
#             'synced': False
#         }
#         self.pending_changes.append(change)
#         self._save_pending_changes()

#     async def synchronize(self, db: Session) -> Dict[str, Any]:
#         from app.db.session import db_manager
#         if not db_manager.check_online_connection():
#             return {
#                 'success': False,
#                 'message': 'No internet connection available',
#                 'pending_changes': len(self.pending_changes)
#             }

#         results = {
#             'success': True,
#             'synced': 0,
#             'failed': 0,
#             'errors': []
#         }

#         for change in self.pending_changes:
#             if change['synced']:
#                 continue

#             try:
#                 # Use SQLAlchemy models instead of raw SQL
#                 model_class = self._get_model_class(change['table'])
#                 if change['operation'] == 'INSERT':
#                     obj = model_class(**change['data'])
#                     db.add(obj)
#                 elif change['operation'] == 'UPDATE':
#                     obj = db.query(model_class).get(change['data']['id'])
#                     for key, value in change['data'].items():
#                         setattr(obj, key, value)
#                 elif change['operation'] == 'DELETE':
#                     obj = db.query(model_class).get(change['data']['id'])
#                     db.delete(obj)

#                 results['synced'] += 1
#                 change['synced'] = True

#             except Exception as e:
#                 results['failed'] += 1
#                 results['errors'].append({
#                     'change': change,
#                     'error': str(e)
#                 })
#                 results['success'] = False

#         if results['synced'] > 0:
#             try:
#                 db.commit()
#             except Exception as e:
#                 db.rollback()
#                 results['success'] = False
#                 results['errors'].append({
#                     'message': 'Commit failed',
#                     'error': str(e)
#                 })

#         self._save_pending_changes()
#         return results

#     def get_status(self) -> Dict[str, Any]:
#         """Get current sync status"""
#         from app.db.session import db_manager
#         return {
#             'pending_changes': len([c for c in self.pending_changes if not c['synced']]),
#             'is_online': db_manager.is_online,
#             'total_changes': len(self.pending_changes),
#             'last_sync': max(
#                 [c['timestamp'] for c in self.pending_changes if c['synced']], 
#                 default=None
#             ),
#             'sync_location': str(self.sync_dir)
#         }

#     def clear_synced_changes(self) -> int:
#         """Clear all synced changes and return number of changes cleared"""
#         original_length = len(self.pending_changes)
#         self.pending_changes = [c for c in self.pending_changes if not c['synced']]
#         self._save_pending_changes()
#         return original_length - len(self.pending_changes)

# # Create global instance
# sync_manager = SyncManager()

# # Export commonly used functions
# get_sync_status = sync_manager.get_status
# synchronize_data = sync_manager.synchronize
# record_change = sync_manager.record_change
# clear_synced_changes = sync_manager.clear_synced_changes

# __all__ = [
#     'sync_manager',
#     'get_sync_status',
#     'synchronize_data',
#     'record_change',
#     'clear_synced_changes'
# ]


from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path
from sqlalchemy.orm import Session

# Create base directory for offline storage
OFFLINE_DB_DIR = Path(__file__).parent.parent / 'offline_db'
OFFLINE_DB_DIR.mkdir(exist_ok=True)

class SyncManager:
    def __init__(self):
        self.sync_dir = OFFLINE_DB_DIR / 'sync'
        self.sync_dir.mkdir(exist_ok=True)
        self.pending_file = self.sync_dir / 'pending_changes.json'
        self.pending_changes: List[Dict[str, Any]] = []
        self._load_pending_changes()

    def _load_pending_changes(self) -> None:
        """Load pending changes from file"""
        try:
            if self.pending_file.exists():
                with open(self.pending_file, 'r') as f:
                    self.pending_changes = json.load(f)
            else:
                self.pending_changes = []
                self._save_pending_changes()
        except Exception as e:
            print(f"Error loading pending changes: {e}")
            self.pending_changes = []

    def _save_pending_changes(self) -> None:
        """Save pending changes to file"""
        try:
            with open(self.pending_file, 'w') as f:
                json.dump(self.pending_changes, f)
        except Exception as e:
            print(f"Error saving pending changes: {e}")

    def record_change(
        self, 
        table_name: str, 
        operation: str, 
        data: Dict[str, Any]
    ) -> None:
        """Record a change for later synchronization"""
        change = {
            'timestamp': datetime.utcnow().isoformat(),
            'table': table_name,
            'operation': operation,
            'data': data,
            'synced': False
        }
        self.pending_changes.append(change)
        self._save_pending_changes()

    async def synchronize(self, db: Session) -> Dict[str, Any]:
        from app.db.session import db_manager
        if not db_manager.check_online_connection():
            return {
                'success': False,
                'message': 'No internet connection available',
                'pending_changes': len(self.pending_changes)
            }

        results = {
            'success': True,
            'synced': 0,
            'failed': 0,
            'errors': []
        }

        for change in self.pending_changes:
            if change['synced']:
                continue

            try:
                # Use SQLAlchemy models instead of raw SQL
                model_class = self._get_model_class(change['table'])
                if change['operation'] == 'INSERT':
                    obj = model_class(**change['data'])
                    db.add(obj)
                elif change['operation'] == 'UPDATE':
                    obj = db.query(model_class).get(change['data']['id'])
                    for key, value in change['data'].items():
                        setattr(obj, key, value)
                elif change['operation'] == 'DELETE':
                    obj = db.query(model_class).get(change['data']['id'])
                    db.delete(obj)

                results['synced'] += 1
                change['synced'] = True

            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'change': change,
                    'error': str(e)
                })
                results['success'] = False

        if results['synced'] > 0:
            try:
                db.commit()
            except Exception as e:
                db.rollback()
                results['success'] = False
                results['errors'].append({
                    'message': 'Commit failed',
                    'error': str(e)
                })

        self._save_pending_changes()
        return results

    def get_status(self) -> Dict[str, Any]:
        """Get current sync status"""
        from app.db.session import db_manager
        return {
            'pending_changes': len([c for c in self.pending_changes if not c['synced']]),
            'is_online': db_manager.is_online,
            'total_changes': len(self.pending_changes),
            'last_sync': max(
                [c['timestamp'] for c in self.pending_changes if c['synced']], 
                default=None
            ),
            'sync_location': str(self.sync_dir)
        }

    def clear_synced_changes(self) -> int:
        """Clear all synced changes and return number of changes cleared"""
        original_length = len(self.pending_changes)
        self.pending_changes = [c for c in self.pending_changes if not c['synced']]
        self._save_pending_changes()
        return original_length - len(self.pending_changes)

# Create global instance
sync_manager = SyncManager()

# Export commonly used functions
get_sync_status = sync_manager.get_status
synchronize_data = sync_manager.synchronize
record_change = sync_manager.record_change
clear_synced_changes = sync_manager.clear_synced_changes

__all__ = [
    'sync_manager',
    'get_sync_status',
    'synchronize_data',
    'record_change',
    'clear_synced_changes'
]