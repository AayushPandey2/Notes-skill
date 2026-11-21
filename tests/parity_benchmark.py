"""Reproducible migration measurements; test tooling, never a runtime dependency."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scriptorium.engines.vault import validate_obsidian_properties
from scriptorium.engines.composition.visuals import scientific_svg

def samples(run, count=1):
    run()
    result=[]
    for _ in range(7):
        start=time.perf_counter()
        for _ in range(count): run()
        result.append((time.perf_counter()-start)*1000/count)
    return {"median_ms":statistics.median(result),"samples_ms":result}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--measure",type=Path,required=True)
    args=p.parse_args()
    binary=args.binary.resolve(strict=True)
    measure=args.measure.resolve(strict=True)
    def command(argv):
        subprocess.run(argv,cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    note="---\ntopic: Quadratics\ntags: [topic/quadratics]\nmaster_topic: Mathematics\ndomain: Mathematics\nnote_type: deep-notes\n---\n# Quadratics\n"
    points=[(-2,4),(-1,1),(0,0),(1,1),(2,4)]
    python={
        "startup_help":samples(lambda:command([sys.executable,"scripts/scribe.py","--help"])),
        "scientific_svg_generation":samples(lambda:scientific_svg({"square":points},title="Quadratic growth",xlabel="x",ylabel="square"),100),
        "properties_validation":samples(lambda:validate_obsidian_properties(note),100),
        "sha256_64k":samples(lambda:hashlib.sha256(bytes([42])*65536).hexdigest(),1000),
    }
    rust=json.loads(subprocess.check_output([str(measure)],text=True,encoding="utf-8"))
    rust={key:({"median_ms":statistics.median(value),"samples_ms":value} if isinstance(value,list) else value) for key,value in rust.items()}
    rust["startup_help"]=samples(lambda:command([str(binary),"--help"]))
    report={"captured_at":datetime.now(timezone.utc).isoformat(),"platform":platform.platform(),"build_profile":"release","python":python,"rust":rust,
        "limits":["Help commands expose different command sets; this only measures launch/import/help overhead.","SVG layouts differ; numerical geometry parity is checked separately. Rust render also performs strict SVG inspection.","Properties validation implementations have different supported schemas; this fixture is accepted by both.","Local filesystem/cache samples include OS caching. Other development processes may affect timings.","No model, network, source discovery, full research or end-to-end educational performance claim is made."]}
    path=ROOT/"docs/rust-migration-benchmarks.json"
    path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"report":str(path),"python_help_ms":python["startup_help"]["median_ms"],"rust_help_ms":rust["startup_help"]["median_ms"]},indent=2))

if __name__=="__main__":main()
