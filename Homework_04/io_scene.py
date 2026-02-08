import json
from objects import SphereObject, BoxObject


def save_scene(scene, filename="scene.json"):
    data = {
        'version': '1.0',
        'objects': []
    }
    
    for obj in scene.objects:
        data['objects'].append(obj.to_dict())
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Scene saved to {filename} ({len(scene.objects)} objects)")


def load_scene(scene, filename="scene.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    
        scene.clear()
        
        for obj_data in data.get('objects', []):
            obj_type = obj_data.get('type')
            
            if obj_type == 'sphere':
                obj = SphereObject.from_dict(obj_data)
                scene.add_object(obj)
            elif obj_type == 'box':
                obj = BoxObject.from_dict(obj_data)
                scene.add_object(obj)
            else:
                print(f"Warning: Unknown object type '{obj_type}', skipping")
        
        print(f"Scene loaded from {filename} ({len(scene.objects)} objects)")
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filename}': {e}")
        return False
    except Exception as e:
        print(f"Error loading scene: {e}")
        return False
