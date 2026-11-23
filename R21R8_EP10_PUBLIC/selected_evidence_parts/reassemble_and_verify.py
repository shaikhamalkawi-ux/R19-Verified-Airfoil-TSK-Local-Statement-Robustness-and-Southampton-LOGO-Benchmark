#!/usr/bin/env python3
import hashlib
from pathlib import Path
from zipfile import ZipFile
root=Path(__file__).resolve().parent
parts=[root / f'H3Air_EP10_public_evidence.zip.part{i:03d}' for i in range(1,20)]
checks={}
for line in (root/'PARTS_SHA256SUMS.txt').read_text().splitlines():
 if '  ' in line:
  h,name=line.split('  ',1);checks[name]=h
assert all(x.exists() for x in parts),'A required part is missing'
for p in parts:
 assert hashlib.sha256(p.read_bytes()).hexdigest()==checks[p.name],f'Part SHA mismatch: {p.name}'
data=b''.join(x.read_bytes() for x in parts)
name='57H3Air_R21R8_EP10_PUBLIC_EVIDENCE_SOURCE_AUDITED.zip'
assert len(data)==13508700,'ZIP size mismatch'
assert hashlib.sha256(data).hexdigest()==checks[name],'ZIP SHA mismatch'
out=root/name;out.write_bytes(data)
with ZipFile(out) as z:
 assert z.testzip() is None
 for line in z.read('SHA256SUMS.txt').decode().splitlines():
  if line.startswith('#') or not line.strip():continue
  sha,filename=line.split('  ',1)
  assert hashlib.sha256(z.read(filename)).hexdigest()==sha,filename
 print('PASS: reconstructed',out.name,'with',len(z.namelist()),'verified ZIP entries')
