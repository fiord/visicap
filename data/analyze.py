import dpkt
import socket
import sys
import pickle
import re

def splitTo5tuples(filename):
    pcr = dpkt.pcap.Reader(open(filename, "rb"))
    res = {}
    line = 0
    for t, buf in pcr:
        line += 1
        eth = dpkt.ethernet.Ethernet(buf)
        dat = eth.data
        if type(dat) in [dpkt.ip.IP, dpkt.ip6.IP6]:
            print(dat.src, dat.dst)
            f = lambda x: socket.inet_ntop(socket.AF_INET if len(dat.src) == 4 else socket.AF_INET6, x)
            src_a = f(dat.src)
            dst_a = f(dat.dst)
            prot = dat.p
            # TODO: ip packet with more flagment
            if type(dat) == dpkt.ip.IP and (dat.mf or dat.offset > 0):
                continue
            dat = dat.data
            print(line, type(dat), prot)
            src_p = dst_p = -1
            try:
                src_p = dat.sport
                dst_p = dat.dport
            except:
                pass
            tuples = (src_a, src_p, dst_a, dst_p, prot)
            if tuples not in res:
                res[tuples] = [(t, dat.data)]
            else:
                res[tuples].append((t, dat.data))
    return res

if __name__ == "__main__":
    filename = "./pcap/n056_20191111_000002.pcap"
    output = re.sub(r"\.pcap$", ".bin", filename)
    tuples = splitTo5tuples(filename)
    with open(output, "wb") as f:
        pickle.dump(tuples, f)
