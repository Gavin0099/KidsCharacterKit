"""Read-only schemas and real source/derivative validators for this checkpoint."""
import json
import subprocess
import sys
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[3]

def main():
    groups=[(ROOT/'manifests/character-manifest.schema.json',[ROOT/'manifests/characters.json']),
            (ROOT/'provenance/schema/provenance.schema.json',[p for p in (ROOT/'provenance').glob('*/*.json') if p.name!='provenance.schema.json']+list((ROOT/'concepts').glob('**/*.provenance.json'))),
            (ROOT/'manifests/animation-manifest.schema.json',list((ROOT/'concepts/kck-03c1').glob('*pack.json'))),
            (ROOT/'manifests/animation-frame-provenance.schema.json',list((ROOT/'concepts/kck-03c1/evidence').glob('*frame-*.json')))]
    validated=[]
    for schema,records in groups:
        validator=Draft202012Validator(json.loads(schema.read_text()));validator.check_schema(validator.schema)
        for path in sorted(records):
            validator.validate(json.loads(path.read_text()));validated.append(str(path.relative_to(ROOT)))
    print(json.dumps({'schemas':'PASS','records':len(validated),'paths':validated}))
    for command in [['concepts/kck-03b/tools/validate_raster.py'],['concepts/kck-03c/tools/validate_animation.py','concepts/kck-03c1/dinosaur-snack-partial-pack.json'],['concepts/kck-03c/tools/validate_animation.py','concepts/kck-03c1/cat-snack-candidate-pack.json']]:
        subprocess.run([sys.executable,*command],cwd=ROOT,check=True)

if __name__=='__main__':main()
