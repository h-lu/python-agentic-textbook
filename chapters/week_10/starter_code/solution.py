"""Week 10 作业参考实现聚合模块。"""

try:
    from practice1_json_basics import (
        create_courses_data,
        create_student_data,
        json_string_roundtrip,
        read_json_file,
        write_json_file,
    )
    from practice2_data_exchange import convert_format, export_data, import_data
    from practice3_serialization import deserialize_event, serialize_event
    from practice4_defensive_programming import (
        load_books_collection,
        safe_load_json,
        validate_book_data,
    )
    from practice5_data_migration import detect_version, migrate_data, migrate_v1_to_v2
    from practice6_config_manager import ConfigManager
    from student_manager_fixed import add_student, find_student, load_students, save_students
except ImportError:  # pragma: no cover - package import fallback
    from .practice1_json_basics import (
        create_courses_data,
        create_student_data,
        json_string_roundtrip,
        read_json_file,
        write_json_file,
    )
    from .practice2_data_exchange import convert_format, export_data, import_data
    from .practice3_serialization import deserialize_event, serialize_event
    from .practice4_defensive_programming import (
        load_books_collection,
        safe_load_json,
        validate_book_data,
    )
    from .practice5_data_migration import detect_version, migrate_data, migrate_v1_to_v2
    from .practice6_config_manager import ConfigManager
    from .student_manager_fixed import add_student, find_student, load_students, save_students
