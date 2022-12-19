const p = ["Classic", "Medium Core", "Hard Core", "Journey"],
            S = (c, g) => {
                const m = g + 1 + c.readInt8(g);
                return [c.toString("utf8", g + 1, m), m]
            },
            o = c => {
                const g = (E => {
                    "string" == typeof E && (E = T.from(E, "ascii"));
                    const L = Z.createDecipheriv("aes-128-cbc", "h\x003\0y\0_\0g\0U\0y\0Z\0", "h\x003\0y\0_\0g\0U\0y\0Z\0");
                    try {
                        return T.concat([L.update(E), L.final()])
                    } catch (G) {
                        throw new Error(`Invalid character data: ${G}`)
                    }
                })(c);
                console.log("player file decrypted");
                const version = g.readInt16LE();
                if (console.log("version: " + version), 234 > version) throw new Error(`This library only supports 4.1.2 (and others with the same format) (version id = ${version})`);
                let offset = 24;
                [, offset] = S(g, offset);
                const M = p[g.readUInt8(offset)] || "Unknown!";
                if ("Journey" !== M) throw new Error(`This only supports Journey Mode characters, not ${M}`);
                for (offset += version < 271 ? 2460 : 2691; - 1 !== g.readInt32LE(offset);) {   
                    offset += 12, [, offset] = S(g, offset);
                }
                offset += 107;
                const P = O.cloneDeep(A);
                for (;;) {
                    let E;
                    if ([E, offset] = S(g, offset), 0 === E.length) break;
                    const L = g.readInt32LE(offset);
                    offset += 4, P[E] ? (P[E].has = L, P[E].researched = A[E].needed <= L) : console.warn(`Uh oh! Missing item: ${E}`)
                }
                return P
            },
            v = c => O.chain(o(c)).pickBy(g => g.researched).keys().value(),
            y = c => O.chain(o(c)).pickBy(g => !g.researched).keys().value(),
            f = c => {
                const g = v(c);
                return O.map(g, m => A[m].id)
            },
            l = c => {
                const g = y(c);
                return O.map(g, m => A[m].id)
            }
