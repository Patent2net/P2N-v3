(this.webpackJsonpapp = this.webpackJsonpapp || []).push([[3], [, , , , , , , , , , , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return S
    })), r.d(t, "d", (function () {
        return F
    })), r.d(t, "c", (function () {
        return C
    })), r.d(t, "e", (function () {
        return T
    })), r.d(t, "f", (function () {
        return L
    })), r.d(t, "b", (function () {
        return z
    }));
    var a = r(5), n = r(7), i = r.n(n), s = r(27), o = r(16), c = r(4), l = r(45), u = r(14), d = r(50), h = r(29),
        m = r(43), p = r(54);

    function b(e, t, r) {
        var n = Object(a.a)(Object(a.a)({}, e), {}, {documents: t.map((e => r.reduce(((t, r) => Object(a.a)(Object(a.a)({}, t), {}, {[r]: e[r] + ""})), {})))});
        return fetch(Object(p.a)(), {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(n)
        }).catch((function (e) {
            return {statusText: Object(m.a)("Failed to connect to the DCS at ".concat(Object(p.a)(), ": ").concat(e.message))}
        })).then((function (e) {
            if (!e.ok) throw e;
            return e.json()
        })).then((function (e) {
            return i(e.clusters, ""), function (e, t) {
                var r = new Set;
                if (t.forEach((e => {
                    e.uniqueDocuments.forEach(r.add.bind(r))
                })), r.size < e.length) {
                    var a = e.map(((e, t) => t)).filter((e => !r.has(e)));
                    t.push({
                        id: "unclustered",
                        labels: ["Other topics "],
                        documents: a,
                        uniqueDocuments: a,
                        size: a.length,
                        unclustered: !0
                    })
                }
            }(t, e.clusters), e
        }));

        function i(e, t) {
            var r, a = 0, n = Object(s.a)(e);
            try {
                for (n.s(); !(r = n.n()).done;) {
                    var o = r.value, c = o.clusters || [], l = o.documents || [];
                    i(c, t + a + "."), o.uniqueDocuments = Array.from(c.reduce((function e(t, r) {
                        (r.clusters || []).reduce(e, t);
                        var a, n = Object(s.a)(r.documents);
                        try {
                            for (n.s(); !(a = n.n()).done;) {
                                var i = a.value;
                                t.add(i)
                            }
                        } catch (o) {
                            n.e(o)
                        } finally {
                            n.f()
                        }
                        return t
                    }), new Set(l))), o.id = t + a++, o.size = o.uniqueDocuments.length
                }
            } catch (u) {
                n.e(u)
            } finally {
                n.f()
            }
        }
    }

    var g = r(32), j = r(17), f = r(112), x = r(22), v = r(56), O = Object(f.a)(), y = (e, t) => {
        var r, a = {source: e, docs: t}, n = window.location.hash.substring(1);
        (r = x.a.workbench.match(n)) ? (a.app = "workbench", a.view = v.a.clusterView) : (r = x.a.searchResults.match(n)) && (a.app = "search", a.view = r.params.view), O.emit("clusteringRequested", a)
    };
    import(new URL("customizer.js", window.location).toString()).then((e => {
        e.default({on: O.on, off: O.off})
    }));
    var w = [], S = Object(u.b)("clusteringAlgorithm", {
        clusteringAlgorithm: void 0,
        getAlgorithmInstance: () => h.a[S.clusteringAlgorithm]
    });
    h.a[S.clusteringAlgorithm] || (S.clusteringAlgorithm = Object.keys(h.a)[0]);
    var F = Object(c.d)({
        loading: !1, clusters: w, documents: w, serviceInfo: null, getClusteredDocsRatio: () => {
            var e = F.clusters.reduce((function e(t, r) {
                return r.unclustered || (r.documents.forEach((e => t.add(e))), r.clusters.reduce(e, t)), t
            }), new Set), t = F.documents.length;
            return t > 0 ? e.size / t : 0
        }
    }), C = (e = !1, t) => {
        var r = S.getAlgorithmInstance(), a = r.getSettings(), n = r.getDefaults(),
            i = Object(j.c)(a, a[0].get, e ? (e, t) => {
                var r = n[e.id];
                return !(Array.isArray(t) ? Object(l.a)(t, r) : t === r)
            } : null);
        t && t.trim().length > 0 && r.applyQueryHint(i, t);
        var s = r.getLanguage();
        return {algorithm: S.clusteringAlgorithm, language: s, parameters: i}
    }, k = function () {
        var e = Object(o.a)(i.a.mark((function e(t) {
            var r, a, n, o, c, l;
            return i.a.wrap((function (e) {
                for (; ;) switch (e.prev = e.next) {
                    case 0:
                        if (l = function (e, t) {
                            var r, a = t.reduce((function e(t, r) {
                                var a, n = Object(s.a)(r.uniqueDocuments);
                                try {
                                    for (n.s(); !(a = n.n()).done;) {
                                        i(t, a.value, r)
                                    }
                                } catch (o) {
                                    n.e(o)
                                } finally {
                                    n.f()
                                }
                                return (r.clusters || w).reduce(e, t);

                                function i(e, t, r) {
                                    e.has(t) ? e.get(t).push(r) : e.set(t, [r])
                                }
                            }), new Map), n = Object(s.a)(e);
                            try {
                                for (n.s(); !(r = n.n()).done;) {
                                    var i = r.value;
                                    i.clusters = a.get(i.__id)
                                }
                            } catch (o) {
                                n.e(o)
                            } finally {
                                n.f()
                            }
                            return e
                        }, r = t.documents, a = t.query, 0 !== r.length) {
                            e.next = 9;
                            break
                        }
                        F.clusters = w, F.documents = w, F.loading = !1, e.next = 37;
                        break;
                    case 9:
                        return F.loading = !0, F.error = void 0, y(t.sourceId, r.length), e.prev = 12, n = t.source.getFieldsToCluster(), o = C(!1, a), e.next = 17, b(o, r, n);
                    case 17:
                        c = e.sent, F.clusters = c.clusters, F.serviceInfo = c.serviceInfo, F.documents = l(r, F.clusters), e.next = 36;
                        break;
                    case 23:
                        return e.prev = 23, e.t0 = e.catch(12), F.clusters = w, F.documents = w, e.prev = 27, e.next = 30, e.t0.json();
                    case 30:
                        e.t0.bodyParsed = e.sent, e.next = 35;
                        break;
                    case 33:
                        e.prev = 33, e.t1 = e.catch(27);
                    case 35:
                        d.a.addError(Object(g.d)(e.t0));
                    case 36:
                        F.loading = !1;
                    case 37:
                    case"end":
                        return e.stop()
                }
            }), e, null, [[12, 23], [27, 33]])
        })));
        return function (t) {
            return e.apply(this, arguments)
        }
    }(), T = function () {
        var e = Object(o.a)(i.a.mark((function e() {
            var t;
            return i.a.wrap((function (e) {
                for (; ;) switch (e.prev = e.next) {
                    case 0:
                        t = L.searchResult, setTimeout(Object(o.a)(i.a.mark((function e() {
                            return i.a.wrap((function (e) {
                                for (; ;) switch (e.prev = e.next) {
                                    case 0:
                                        return e.abrupt("return", k(t));
                                    case 1:
                                    case"end":
                                        return e.stop()
                                }
                            }), e)
                        }))), 0);
                    case 2:
                    case"end":
                        return e.stop()
                }
            }), e)
        })));
        return function () {
            return e.apply(this, arguments)
        }
    }(), L = Object(c.d)({
        loading: !1,
        error: !1,
        initial: !0,
        searchResult: {query: "", matches: 0, documents: w},
        load: function () {
            var e = Object(o.a)(i.a.mark((function e(t, r, a) {
                return i.a.wrap((function (e) {
                    for (; ;) switch (e.prev = e.next) {
                        case 0:
                            return L.loading = !0, L.error = !1, e.prev = 2, L.initial = !1, e.t0 = I, e.next = 7, r.source(a);
                        case 7:
                            e.t1 = e.sent, e.t2 = t, e.t3 = r, L.searchResult = (0, e.t0)(e.t1, e.t2, e.t3), e.next = 22;
                            break;
                        case 13:
                            return e.prev = 13, e.t4 = e.catch(2), e.t5 = d.a, e.next = 18, r.createError(e.t4);
                        case 18:
                            e.t6 = e.sent, e.t5.addError.call(e.t5, e.t6), L.error = !0, L.searchResult = {
                                query: a,
                                matches: 0,
                                documents: w
                            };
                        case 22:
                            L.loading = !1;
                        case 23:
                        case"end":
                            return e.stop()
                    }
                }), e, null, [[2, 13]])
            })));
            return function (t, r, a) {
                return e.apply(this, arguments)
            }
        }()
    });

    function I(e, t, r) {
        return Object(a.a)(Object(a.a)({}, e), {}, {
            sourceId: t,
            source: r,
            documents: (e.documents || []).map(((t, r) => Object(a.a)(Object(a.a)({}, t), {}, {
                __id: r,
                __rank: 1 - r / e.documents.length
            })))
        })
    }

    Object(c.a)(Object(o.a)(i.a.mark((function e() {
        return i.a.wrap((function (e) {
            for (; ;) switch (e.prev = e.next) {
                case 0:
                    return e.next = 2, T();
                case 2:
                case"end":
                    return e.stop()
            }
        }), e)
    })))), Object(c.a)((() => {
        L.loading && (F.loading = !0, F.clusters = w)
    }));
    var z = (e, t) => {
        var r = L.searchResult.query.replace(/[\s:]+/g, "_").replace(/[+-\\"'/\\?]+/g, ""), a = L.searchResult.sourceId;
        return "".concat(a, "-").concat(r).concat(r.length > 0 ? "-" : "").concat(e, ".").concat(t)
    }
}, function (e, t, r) {
    "use strict";
    r.d(t, "d", (function () {
        return c
    })), r.d(t, "a", (function () {
        return l
    })), r.d(t, "c", (function () {
        return u
    })), r.d(t, "b", (function () {
        return d
    })), r.d(t, "e", (function () {
        return h
    }));
    var a = r(0), n = (r(1), r(209), r(40)), i = r(15), s = r(11), o = r(65), c = e => !e.visible || e.visible(),
        l = ({label: e, description: t}) => t ? Object(a.jsxs)("div", {
            className: "LabelWithHelp",
            children: [e, Object(a.jsx)(u, {description: t})]
        }) : e, u = ({description: e}) => Object(a.jsx)(o.a, {
            description: e,
            children: Object(a.jsx)(i.a, {className: "HelpIcon", icon: s.t})
        }), d = ({className: e, inline: t = !1, label: r, description: i, message: s, children: o}) => {
            var c;
            return s && (c = Object(a.jsx)("div", {
                className: "SettingMessage",
                children: s
            })), Object(a.jsxs)(n.d, {
                className: "".concat(e, " Setting"),
                inline: t,
                label: Object(a.jsx)(l, {label: r, description: i}),
                children: [o, c]
            })
        }, h = (e, t) => ({get: () => e[t], set: (r, a) => e[t] = a})
}, function (e, t, r) {
    "use strict";
    r.d(t, "b", (function () {
        return c
    })), r.d(t, "a", (function () {
        return l
    }));
    var a = r(4), n = r(62), i = r.n(n), s = r(101), o = r.n(s), c = (e, t, r) => {
        var n = Object(a.d)(Object.assign({}, t, i.a.get(e), r));
        return Object(a.a)((function () {
            i.a.set(e, n)
        })), n.resetToDefaults = () => {
            Object.keys(t).forEach((e => {
                n[e] = t[e]
            }))
        }, n.getDefaults = () => t, n
    }, l = (e, t, r, n = 1024) => {
        var s = new o.a({max: n});
        return s.load(i.a.get(e) || []), Object(a.a)((() => {
            var a = r();
            if (a) {
                var n = t(a);
                n && (s.set(n, a), i.a.set(e, s.dump()))
            }
        })), s
    }
}, , , function (e, t, r) {
    "use strict";
    r.d(t, "f", (function () {
        return w
    })), r.d(t, "g", (function () {
        return C
    })), r.d(t, "h", (function () {
        return k
    })), r.d(t, "i", (function () {
        return T
    })), r.d(t, "b", (function () {
        return L
    })), r.d(t, "c", (function () {
        return I
    })), r.d(t, "a", (function () {
        return z
    })), r.d(t, "d", (function () {
        return R
    })), r.d(t, "e", (function () {
        return D
    }));
    var a = r(5), n = r(0), i = (r(1), r(210), r(107)), s = r.n(i), o = r(44), c = r(4), l = r(13), u = r(49),
        d = r(40), h = r(38), m = r(65), p = r(66), b = r(11), g = r(15),
        j = Object(c.e)((({setting: e, get: t, set: r, type: a}) => {
            var i = () => t(e).find((e => Array.isArray(e[a])));
            return Object(n.jsx)(d.s, {
                style: {width: "100%", minHeight: "8rem"}, value: (() => {
                    var e = i();
                    return e ? e[a].join("\r") : ""
                })(), onChange: n => (n => {
                    var s = i(), o = n.trim().length > 0 ? n.split("\n") : [];
                    s ? s[a] = o : t(e).push({[a]: o}), r(e, t(e).slice(0))
                })(n.target.value)
            })
        })), f = (e, t, r, a) => Object(n.jsx)(j, {setting: t, get: r, set: a, type: e}), x = (e, t, r, a) => ({
            label: e,
            createContentElement: (e, {
                setting: i,
                get: s,
                set: o
            }) => Object(n.jsxs)(n.Fragment, {
                children: [t(i, s, o), Object(n.jsxs)("div", {
                    className: "ExclusionsSettingInlineHelp",
                    children: [r, ",", " ", Object(n.jsx)(m.a, {
                        description: a,
                        children: Object(n.jsx)(h.a, {children: "syntax help"})
                    })]
                })]
            }),
            tools: [{
                createContentElement: ({
                                           setting: e,
                                           get: t
                                       }) => Object(n.jsx)(p.a, {
                    contentProvider: () => JSON.stringify(t(e), null, 2),
                    buttonText: "Copy JSON",
                    buttonProps: {
                        small: !0,
                        minimal: !0,
                        title: "Copy dictionaries JSON",
                        icon: Object(n.jsx)(g.a, {icon: b.b})
                    }
                })
            }]
        }), v = e => {
            var t = {
                glob: x("glob", ((e, t, r) => f("glob", e, t, r)), Object(n.jsxs)("span", {children: ["One pattern per line, separate words with spaces, ", Object(n.jsx)("code", {children: "*"}), " is zero or more words"]}), '\n<p>\n  Glob patterns allow simple word-based wildcard matching. Use them for case-insensitive\n  matching of literal phrases, as well as "begins with\u2026", "ends with\u2026" or "contains\u2026"\n  types of expressions. Glob patterns are fast to parse and very fast to apply.\n</p>\n\n<h4>Pattern syntax and matching rules</h4>\n\n<ul>\n  <li>Put one entry per line.</li>\n  <li>Each entry must consist of one or more space-separated tokens.</li>\n  <li>A token can be a sequence of arbitrary characters, such as words, numbers, identifiers.</li>\n  <li>Matching is case-insensitive by default.</li>\n  <li>The <code>*</code> token matches zero or more words.</li>\n  <li>\n    Using the <code>*</code> wildcard character in combination with other characters, for\n    example 1<code>programm*</code>, is not supported.\n  </li>\n  <li>\n    Token put in double quotes, for example <code>"Rating***"</code> is taken literally: matching\n    is case-sensitive, <code>*</code> characters are allowed and taken literally.\n  </li>\n  <li>\n    To include double quotes as part of the token, escape them with the <code>\\</code> character,\n    for example: <code>\\"information\\"</code>.\n  </li>\n</ul>\n\n<h4>Example patterns</h4>\n\n<dl>\n  <dt><code>more information</code> (exact match)</dt>\n  <dd>\n    Matches:\n    <ul>\n      <li><code>more information</code></li>\n      <li><code>More information</code></li>\n      <li><code>MORE INFORMATION</code></li>\n    </ul>\n\n    Does not match:\n\n    <ul>\n      <li><code title="\'informations\' does not match pattern token \'information\'.">more informations</code><br/></li>\n      <li><code title="Pattern does not contain wildards, only 2-word strings can match.">more information about</code><br/></li>\n      <li><code title="Pattern does not contain wildards, only 2-word strings can match.">some more information</code></li>\n    </ul>\n  </dd>\n\n  <dt><code>more information *</code> (leading match)</dt>\n  <dd>\n    Matches:\n    <ul>\n      <li><code>more information</code></li>\n      <li><code>More information about</code></li>\n      <li><code>More information about a</code></li>\n    </ul>\n\n    Does not match:\n\n    <ul>\n      <li title="\'informations\' does not match pattern token \'information\'."><code>informations</code></li>\n      <li title="\'informations\' does not match pattern token \'information\'."><code>more informations about</code></li>\n      <li title="\'informations\' does not match pattern token \'information\'."><code>some more informations</code></li>\n    </ul>\n  </dd>\n\n  <dt><code>* more information *</code> (containing match)</dt>\n  <dd>\n    Matches:\n    <ul>\n      <li><code>information</code></li>\n      <li><code>more information</code></li>\n      <li><code>information about</code></li>\n      <li><code>a lot more information on</code></li>\n    </ul>\n\n    Does not match:\n    <ul>\n      <li title="\'informations\' does not match pattern token \'information\'."><code>informations</code></li>\n      <li title="\'informations\' does not match pattern token \'information\'."><code>more informations about</code></li>\n      <li title="\'informations\' does not match pattern token \'information\'."><code>some more informations</code></li>\n    </ul>\n  </dd>\n\n  <dt><code>"Information" *</code> (literal match)</dt>\n  <dd>\n    Matches:\n    <ul>\n      <li><code>Information</code></li>\n      <li><code>Information about</code></li>\n      <li><code>Information ABOUT</code></li>\n    </ul>\n\n    Does not match:\n    <ul>\n      <li title="&quot;Information&quot; token is case-sensitive, it does not match \'information\'."><code>information</code></li>\n      <li title="&quot;Information&quot; token is case-sensitive, it does not match \'information\'."><code>information about</code></li>\n      <li title="\'Informations\' does not match pattern token &quot;Information&quot;."><code>Informations about</code></li>\n    </ul>\n  </dd>\n\n  <dt><code>"Programm*"</code> (literal match)</dt>\n  <dd>\n    Matches:\n    <ul>\n      <li><code>Programm*</code></li>\n    </ul>\n\n    Does not match:\n    <ul>\n      <li title="&quot;Programm*&quot; token is taken literally, it matches only \'Programm*\'."><code>Programmer</code></li>\n      <li title="&quot;Programm*&quot; token is taken literally, it matches only \'Programm*\'."><code>Programming</code></li>\n    </ul>\n  </dd>\n\n  <dt><code>\\"information\\"</code> (escaping quote characters)</dt>\n  <dd>\n    Matches:\n    <ul>\n      <li><code>"information"</code></li>\n    </ul>\n\n    Does not match:\n    <ul>\n      <li title="Escaped quotes are taken literally, so match is case-insensitive"><code>"INFOrmation"</code></li>\n      <li title="Escaped quotes not found in the string being matched."><code>information</code></li>\n      <li title="Escaped quotes not found in the string being matched."><code>"information</code></li>\n    </ul>\n  </dd>\n\n  <dt><code>programm*</code></dt>\n  <dd>\n    Illegal pattern, combinations of the <code>*</code> wildcard and other characters are not supported.\n  </dd>\n\n  <dt><code>"information</code></dt>\n  <dd>\n    Illegal pattern, unbalanced double quotes.\n  </dd>\n\n  <dt><code>*</code></dt>\n  <dd>\n    Illegal pattern, there must be at least one non-wildcard token.\n  </dd>\n</dl>'),
                exact: x("exact", ((e, t, r) => f("exact", e, t, r)), Object(n.jsx)("span", {children: "One label per line, exact matching"}), '\n<p>\n  Exact patterns require exact, case-sensitive equality between the word or phrase and\n  the dictionary entry. Exact patterns are fast to parse and very fast to apply\n  during clustering.\n</p>\n\n<p>\n  Put one exact pattern per line.\n</p>\n\n<p>\n  For case-insensitive matching, use glob matchers (preferably) or case-insensitive\n  regexp matchers.\n</p>\n\n<h4>Example patterns</h4>\n\n<dl>\n  <dt><code>DevOps</code></dt>\n  <dd>\n    Matches:\n    <ul>\n      <li><code>DevOps</code></li>\n    </ul>\n\n    Does not match:\n\n    <ul>\n      <li><code title="character case does not match\'.">devops</code><br/></li>\n      <li><code>DevOps position</code></li>\n    </ul>\n  </dd>\n</dl>'),
                regex: x("regexp", ((e, t, r) => f("regexp", e, t, r)), Object(n.jsx)("span", {children: "One Java regex per line"}), '\n<p>\n  The regexp patterns check words or phrases against a list of regular expressions you provide.\n  Put one entry per line, use \n  <a href="https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/regex/Pattern.html"\n  target="_blank" >Java regular expressions syntax</a>. If any fragment of a word or phrase matches\n   any regular expression provided in the dictionary, the word or phrase will be filtered out.\n</p>\n\n<p>\n  Regular expression-based matching can result in a dramatic decrease of clustering performance.\n  Use it only when a similar effect cannot be achieved by reasonable number of exact and glob \n  matching entries.\n</p>')
            };
            return e && e(t, x), [{views: t}]
        }, O = Object(c.e)((({setting: e, get: t, set: r, views: a, getActiveView: i, setActiveView: s}) => {
            var o = e.label, c = e.description;
            return Object(n.jsx)(l.b, {
                className: "ExclusionsSetting",
                label: o,
                description: c,
                children: Object(n.jsx)(u.a, {views: a, activeView: i(), onViewChange: s, setting: e, get: t, set: r})
            })
        })), y = r(14), w = e => (e => {
            var t = (e, r) => (Object.keys(e.attributes).forEach((a => {
                var n = e.attributes[a];
                r.push(n), n.attributes && t(n, r), n.implementations && Object.keys(n.implementations).forEach((e => t(n.implementations[e], r)))
            })), r);
            return t(e, [])
        })(e).reduce(((e, t) => (e.set(t.id, t), e)), new Map), S = e => {
            var t = (e => (e || []).reduce(((e, t) => {
                var r = t.split(/\s+/), a = parseFloat(r[2]);
                switch (r[1].charAt(0)) {
                    case">":
                        e.min = a;
                        break;
                    case"<":
                        e.max = a;
                        break;
                    default:
                        throw new Error("Unknown constraint: " + t)
                }
                return e
            }), {}))(e.constraints);
            return Object(a.a)({type: "number"}, t)
        }, F = (e, t) => {
            var r = e.get(t);
            if (r) return r;
            throw new Error("Unknown attribute ".concat(t, "."))
        }, C = (e, t, r) => {
            var a, n = F(e, t), i = {id: t, label: n.description, description: n.javadoc.text, pathRest: n.pathRest};
            if (n.implementations) Object.assign(i, (e => {
                var t = e.implementations;
                return {
                    type: "enum",
                    ui: "select",
                    options: Object.keys(t).map((e => ({value: e, label: e, description: t[e].javadoc.text})))
                }
            })(n)); else if (null === n || void 0 === n || null === (a = n.constraints) || void 0 === a ? void 0 : a[0].startsWith("value in")) Object.assign(i, (e => ({
                type: "enum",
                ui: "select",
                options: e.constraints[0].split(/[[\]]/)[1].split(/,\s*/).map((e => ({value: e, label: e})))
            }))(n)); else switch (n.type) {
                case"Double":
                case"Float":
                    Object.assign(i, S(n));
                    break;
                case"Integer":
                    Object.assign(i, S(n)), i.integer = !0;
                    break;
                case"Boolean":
                    i.type = "boolean";
                    break;
                case"String[]":
                    i.type = "string-array";
                    break;
                default:
                    throw new Error("Unsupported type ".concat(n.type, " for id ").concat(t))
            }
            return Object.assign(i, r)
        }, k = (e, t, r, a = (() => null)) => {
            var n = F(e, t), i = C(e, t, a(n)), s = n.implementations;
            return s && (i.pathRest += ".@type"), s ? [i, ...Object.keys(s).filter((e => {
                var t = s[e].attributes;
                return Object.keys(t).length > 0
            })).map((t => {
                var o = s[t].attributes;
                return {
                    type: "group",
                    id: n.id + ":" + t,
                    visible: () => r()(i) === t,
                    settings: Object.keys(o).map((t => k(e, o[t].id, a))).flat()
                }
            }))] : [i]
        }, T = (e, t, r) => {
            var a = F(e, t), n = C(e, t + ".enabled"), i = Object(o.a)(a.implementations);
            n.description = i.javadoc.text;
            var s = i.attributes, c = Object.keys(s).filter((e => "enabled" !== e)).map((t => C(e, s[t].id)));
            return c.length > 0 ? [n, {type: "group", id: a.id + ":children", visible: () => r()(n), settings: c}] : [n]
        }, L = (e, t) => t.flat().reduce((function t(r, a) {
            return "group" === a.type ? a.settings.reduce(t, r) : r[a.id] = e.get(a.id).value, r
        }), {}), I = (e, t, r) => e.reduce((function e(a, n) {
            if (n.visible && !n.visible()) return a;
            if ("group" === n.type) n.settings.reduce(e, a); else if (n.pathRest) {
                var i = t(n);
                r && !r(n, i) || s()(a, n.pathRest, i)
            }
            return a
        }), {}), z = e => (e.advanced = !0, e), q = (e, t) => {
            var r = Object(y.b)("workbench:settings:".concat(e, ":").concat(t, ":view"), {activeView: "glob"}, {
                get: () => r.activeView,
                set: e => r.activeView = e
            });
            return r
        },
        N = '\n<p>\n  Three pattern types are available:\n</p>\n\n<ul>\n  <li>\n    <strong>glob</strong>: allows simple word-based wildcard matching. \n    Use it for case-insensitive matching of literal phrases, as well as "begins with\u2026", \n    "ends with\u2026" or "contains\u2026" types of expressions.\n  </li>\n  <li>\n    <strong>exact</strong>: requires exact case-sensitive equality between the word or phrase\n    and the dictionary entry.  \n  </li>\n  <li>\n    <strong>regex</strong>: word and phrase filtering based on Java regular expressions.\n  </li>\n</ul>\n\n<p>\n  Combine some or all pattern types as required.\n</p>',
        R = (e, t) => {
            var r = q(e, "labelExclusions"), a = v(t);
            return {
                id: "dictionaries.labelFilters",
                label: "Excluded label patterns",
                pathRest: "dictionaries.labelFilters",
                factory: (e, t, i) => Object(n.jsx)(O, {
                    setting: e,
                    get: t,
                    set: i,
                    views: a,
                    getActiveView: r.get,
                    setActiveView: r.set
                }),
                description: "\n<p>\n  Label exclusion patterns. If a word or a phrase matches any of the patterns provided here,\n  it will not be used as a cluster label.  \n</p>\n\n".concat(N)
            }
        }, D = e => {
            var t = q(e, "wordExclusions"), r = v();
            return {
                id: "dictionaries.wordFilters",
                label: "Stop words",
                pathRest: "dictionaries.wordFilters",
                description: "\n<p>\n  List of words to exclude from processing. If a word is excluded, it will not have\n   influence on the clusters the algorithm creates, but may still appear in cluster \n   labels, such as <em>University of Washington</em>, to aid readability.\n</p>\n\n".concat(N),
                factory: (e, a, i) => Object(n.jsx)(O, {
                    setting: e,
                    get: a,
                    set: i,
                    views: r,
                    getActiveView: t.get,
                    setActiveView: t.set
                })
            }
        }
}, , , , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return i
    }));
    var a = r(73);

    class n {
        constructor(e) {
            this.path = e, this.pathCompiled = Object(a.a)(e), this.match = Object(a.b)(e)
        }

        buildUrl(e) {
            return this.pathCompiled(e)
        }
    }

    var i = {
        about: new n("/about"),
        search: new n("/search"),
        searchStart: new n("/search/:source?"),
        searchResults: new n("/search/:source/:query/:view?"),
        workbench: new n("/workbench")
    }
}, , , , , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return g
    }));
    var a = r(0), n = (r(1), r(31)), i = r(15), s = r(11), o = (r(214), r(6)), c = r.n(o),
        l = ({className: e = ""}) => Object(a.jsx)("svg", {
            className: c()("CarrotLogo Logo", e),
            version: "1.1",
            viewBox: "0 0 116.93 113.72",
            xmlns: "http://www.w3.org/2000/svg",
            children: Object(a.jsxs)("g", {
                transform: "translate(0.511764 .041011)",
                fillOpacity: ".95",
                strokeOpacity: "0.15",
                strokeWidth: "0.5",
                children: [Object(a.jsx)("path", {d: "m48.604 18.807c0.036-0.1771-4.7496-0.07139-6.3086 0.07031-3.544 0.425-6.591 1.0626-9.709 2.0547-10.03 3.26-18.708 9.8126-24.59 18.6-2.551 3.789-4.64 8.1837-5.916 12.471-1.5594 5.1-2.3404 11.483-2.0215 16.16 0.708 9.71 3.8275 18.249 9.3555 25.619 2.874 3.828 6.4876 7.3736 10.35 10.102 5.49 3.933 11.695 6.5892 18.25 7.8652 1.913 0.3898 4.5691 0.74331 6.4121 0.84961v6e-3c1.063 0.1063 4.1095 0.1063 5.1016 0 4.326-0.319 8.2928-1.0626 12.049-2.2676 14.21-4.64 25.474-15.949 30.08-30.119 1.2399-3.76 1.9489-7.4825 2.2324-11.521 0.0709-1.028 0.10571-4.5703 0.07031-4.5703-0.07 0-15.592 5.2804-15.84 5.3867-0.2126 0.106-0.24697 0.10497-0.38867 1.168-0.992 6.21-4.0755 12.23-8.6465 16.801-6.27 6.307-14.742 9.6378-23.459 9.248-6.66-0.319-12.79-2.6228-18.07-6.8398-1.311-1.063-3.7202-3.437-4.7832-4.748-0.886-1.134-2.1256-2.9747-2.7988-4.1797-2.126-3.69-3.473-7.9068-3.9336-12.301-0.1417-1.453-0.14146-4.3238-0.03516-5.6348 0.638-6.34 2.8696-11.94 6.7676-16.83 1.063-1.346 3.5425-3.7905 4.8535-4.8535 2.41-1.914 5.1728-3.5086 8.0078-4.6426 2.445-0.9569 4.3593-1.4512 7.6543-1.9473l0.32031-0.07227 2.5156-7.8652c1.382-4.358 2.4805-7.9724 2.4805-8.0078z"}), Object(a.jsx)("path", {d: "m107.28-0.0058594c-0.355-0.0709-1.5943-0.034278-2.0195 0.10742-1.382 0.389-1.771 0.63611-3.082 1.9121-0.992 0.9567-1.0276 1.0279-1.2402 0.95703-0.106-0.036-1.3818-0.60268-2.7988-1.2051-1.453-0.6022-2.7989-1.1339-3.0469-1.2402-0.708-0.2126-2.3034-0.28267-2.9766-0.10547-0.885 0.212-1.4515 0.53153-2.1602 1.2402l-0.60352 0.60156-3.9688 7.123c-2.161 3.933-4.0017 7.1928-4.0371 7.2637-0.1063 0.1063-0.17753 0.10518-0.95703-0.10742-2.375-0.5669-3.9348-0.74414-6.3438-0.74414-1.878 0-2.8707 0.07231-4.4297 0.32031-6.161 1.027-10.942 4.0743-13.068 8.3613-0.212 0.39-0.85048 1.7712-1.4883 3.1172-0.63 1.34-5.5595 11.9-10.98 23.49-5.424 11.589-9.923 21.262-10.029 21.51-0.3544 1.134-0.35464 2.4468 0.03516 3.5098 0.638 1.7 2.1618 2.9392 3.9688 3.2227l-0.01367 0.0098c0.248 0.0709 0.53237 0.07031 0.63867 0.07031 0.39 0 1.3812-0.14116 1.8418-0.31836 0.28-0.071 5.4565-2.4814 11.48-5.3164 27.395-12.83 35.934-16.798 36.43-16.939 0.425-0.1418 0.77992-0.35385 1.4531-0.81445 1.0276-0.708 1.5246-1.2054 1.8789-1.9141 0.1417-0.284 0.56723-0.95654 0.95703-1.5234 1.488-2.161 2.3022-3.7899 3.1172-6.1289 1.1339-3.334 1.5231-6.9496 1.0625-10.352-0.0708-0.6023-0.10606-0.95679-0.03516-0.99219 0.036-0.035 2.5878-0.53076 5.6348-1.0977 5.2082-0.9571 5.5976-1.0274 6.0938-1.2754 1.382-0.709 2.3382-2.1264 2.5508-3.8984 0.1417-0.957-0.036-2.1268-0.42578-2.9062-0.106-0.212-0.99227-1.7697-1.9844-3.4707-0.9925-1.666-1.7715-3.084-1.7715-3.084 0-0.036 1.7726-1.5231 3.9336-3.3301 2.516-2.055 4.0396-3.4026 4.2168-3.6152 0.567-0.815 0.81446-1.6648 0.81446-2.7988-0.0354-0.992-0.14062-1.5589-0.63672-2.5156l-0.35547-0.74414-2.6914-2.6934c-2.906-2.9055-3.1908-3.1186-4.2188-3.4375-0.2835-0.1063-0.60244-0.21265-0.74414-0.24805zm-0.92383 5.1055c0.142 0 4.5002 4.3585 4.4648 4.4648 0 0.035-3.4373 2.9421-7.6543 6.4141l-7.6172 6.3066h7.1934l0.17774 0.24805c0.319 0.46 3.1875 5.456 3.1875 5.5977 0 0.0709-0.10518 0.17774-0.38868 0.17774-0.49 0.107-15.019 2.7637-15.09 2.7637s0.03462 0.3538 0.35352 1.0625c0.7086 1.665 1.1688 3.6852 1.3105 5.7402 0.248 3.752-0.77814 7.7565-2.8691 10.98-0.602 0.921-1.5952 2.1619-2.1621 2.6934-0.32 0.32-2.5495 1.3788-24.27 11.549l-0.0098 0.0059c-13.15 6.128-23.953 11.23-23.988 11.23-0.0709 0.0709-0.14233 0-0.17773 0-0.03-0.04 4.9982-10.881 11.199-24.061 10.699-22.922 11.231-24.018 11.621-24.408 1.878-1.948 5.1716-3.7557 8.1836-4.5352 4.219-1.028 9.0734-0.42694 12.9 1.6641 0.5315 0.248 0.67358 0.31895 0.70898 0.24805 0.036-0.071 2.3032-4.11 5.0312-9 3.472-6.201 5.0326-8.9297 5.1035-8.9297 0.213 0 4.5697 1.8781 4.6406 1.9844 0.036 0.07-0.67216 1.7356-2.1602 5.1016-1.2403 2.764-2.2327 5.033-2.1973 5.0684 0 0.036 2.7992-2.729 6.2012-6.166 3.437-3.402 6.2712-6.2012 6.3066-6.2012z"})]
            })
        }), u = () => Object(a.jsx)("svg", {
            className: "Carrot2Text Logo",
            version: "1.1",
            viewBox: "0 0 494.77 129.65",
            xmlns: "http://www.w3.org/2000/svg",
            children: Object(a.jsx)("g", {
                transform: "translate(307.84 -83.173)", children: Object(a.jsxs)("g", {
                    transform: "matrix(.27966 0 0 .27966 -450.18 53.969)",
                    fillOpacity: "0.95",
                    children: [Object(a.jsx)("path", {d: "m711.9 565.3q-86.18-0.2711-144.7-58.29-58.26-58.29-58.26-145.9 0.271-85.67 58.53-144 58.26-58.56 144.4-58.56 86.99 0 149.3 54.22l-54.2 59.37q-41.3-32.4-95-32.4-54.74 0.2711-88.34 34.16-33.33 33.89-33.33 86.75 0.271 56.66 33.87 90.01t88.34 33.35 94.58-32.26l54.2 59.37q-62 54.3-149.3 54.3z"}), Object(a.jsx)("path", {d: "m924.2 326.7q51.49-32.53 119.2-32.53 48.78 0 77.23 27.11t28.45 81.33v162.7h-75.88v-21.69q-33.06 21.69-59.62 21.69-54.2 0-81.3-23.04t-27.1-63.71q0-37.96 25.47-67.78 25.74-29.82 82.92-29.82 26.29 0 59.62 16.27v-8.133q-0.542-29.82-43.36-32.53-48.78 0-75.88 16.27l-29.81-46.09zm149 157.2v-30.64q-10.84-20.88-51.49-20.88-48.78 5.422-51.49 37.96 2.71 32.26 51.49 34.97 40.65 0 51.49-21.42z"}), Object(a.jsx)("path", {d: "m1285 324q29-29.82 70.73-29.82 13.28 0 25.2 2.169l-11.92 74.83q-13.28-11.93-37.94-12.74-27.64 1.898-46.07 40.12v166.7h-75.88v-263.2l75.88-8.133v30.09z"}), Object(a.jsx)("path", {d: "m1490 324q29-29.82 70.73-29.82 13.28 0 25.2 2.169l-11.92 74.83q-13.28-11.93-37.94-12.74-27.64 1.898-46.07 40.12v166.7h-75.88v-263.2l75.88-8.133v30.09z"}), Object(a.jsx)("path", {d: "m1739 568q-59.08 0-98.64-39.58-39.56-39.85-39.56-98.68 0-59.1 39.56-98.68 39.57-39.58 98.64-39.58 59.08 0 98.64 39.58t39.56 98.68-39.56 98.68-98.64 39.58zm-0.2711-65.61q30.89 0 50.13-20.6 19.24-20.88 19.24-51.78 0-30.91-19.24-51.78-19.24-20.88-50.4-20.88-30.62 0-49.86 20.88t-19.24 51.78q0 30.91 19.24 51.78 19.24 20.6 50.13 20.6z"}), Object(a.jsx)("path", {d: "m2086 552.5q-19.51 12.74-44.71 12.74-46.07 0-73.17-25.76t-27.1-66.42v-117.4h-40.65v-61.27h40.65v-73.47l76.15-8.133v81.6h40.65v61.27h-40.65v106.5q0 21.69 8.943 30.64 9.214 8.675 23.58 8.675 4.336 0 20.32-3.524l15.99 54.49z"}), Object(a.jsx)("path", {d: "m2194 104.1q36.39 0 59.54 18.37 23.32 18.2 23.32 54.44 0 43.02-33.08 78.76-32.91 35.74-54.41 46.99h89.31v49.64h-167.2v-49.64q16.54 0 62.85-41.37t53.75-58.74q7.443-17.37-0.827-34.75-8.27-17.37-39.69-17.37-29.77 0-46.31 19.86l-33.08-33.09q16.54-16.55 32.25-24.82 15.71-8.273 53.59-8.273z"})]
                })
            })
        }), d = () => Object(a.jsxs)("svg", {
            className: "CarrotSearchText Logo",
            version: "1.1",
            viewBox: "0 0 306.26 91.016",
            xmlns: "http://www.w3.org/2000/svg",
            children: ["Carrot Search logo", Object(a.jsxs)("g", {
                transform: "translate(-124.37 -21.646)",
                strokeOpacity: "0.15",
                strokeWidth: "0.5",
                children: [Object(a.jsx)("path", {
                    className: "carrot",
                    d: "m403.63 82.799-0.0354 14.74c0 8.114 0 14.78 0.0354 14.85 0.0354 0.0709 0.5669 0.0709 2.728 0.0709l2.764-0.0354 0.0354-6.732v-6.661l0.4961-0.4961c0.8858-0.8858 1.878-1.24 3.012-1.098 1.63 0.2126 2.622 1.028 3.154 2.587 0.1417 0.3898 0.1772 0.8504 0.2126 6.413l0.0354 5.988h5.492v-6.732c0-6.732 0-6.732-0.1772-7.406-0.3543-1.382-0.9567-2.445-1.913-3.472-1.382-1.453-3.118-2.126-5.492-2.126-1.736 0-2.976 0.3898-4.252 1.276-0.248 0.1772-0.4961 0.3189-0.5315 0.3189 0 0-0.0354-2.551-0.0354-5.705l-0.0354-5.776h-5.492zm-271.1 9.78c-1.098 0.0709-2.055 0.2835-3.012 0.7795-1.913 0.9567-2.906 2.091-3.366 3.72-0.1417 0.5315-0.2126 0.7795-0.2126 1.878 0 1.063 0.0709 1.382 0.2126 1.878 0.4252 1.524 0.9567 2.232 2.48 2.976 1.276 0.6378 2.126 0.8504 4.571 1.205 1.488 0.2126 2.232 0.5669 2.409 1.169 0.1772 0.6024-0.3543 1.346-1.169 1.63-0.7087 0.2126-1.772 0.3189-2.551 0.2126-1.382-0.2126-2.516-0.6732-3.295-1.417-0.2126-0.1772-0.4606-0.3189-0.4961-0.2835-0.1063 0.0709-2.941 3.331-2.941 3.402 0 0.0709 0.5669 0.6024 1.063 0.9567 1.488 1.098 3.224 1.736 5.244 1.949 0.815 0.0709 2.622 0 3.26-0.1063 1.736-0.3189 3.295-1.098 4.323-2.161 0.9213-1.028 1.311-2.055 1.311-3.685 0-1.559-0.248-2.728-0.8504-3.685-0.815-1.382-2.693-2.339-5.315-2.728-2.197-0.3543-3.472-0.9567-3.472-1.665 0-0.8504 0.9213-1.382 2.587-1.453 1.346-0.0709 2.232 0.248 3.224 1.098 0.2835 0.2126 0.5315 0.4252 0.5315 0.4252 0.0709 0 2.941-3.295 3.012-3.402 0.0354-0.1417-0.7087-0.815-1.488-1.311-1.453-0.9567-2.693-1.311-4.925-1.382-0.3898-0.0354-0.7795-0.0354-1.134 0zm56.02 0.1063c-2.657 0-4.89 0.9213-6.697 2.657-1.453 1.382-2.268 2.976-2.693 5.102-0.2126 1.028-0.2126 3.366 0 4.429 0.4252 1.949 1.276 3.472 2.657 4.854 0.7795 0.7795 1.417 1.276 2.374 1.736 0.9213 0.4606 2.197 0.815 3.366 0.9567 0.1417 0.0354 0.9567 0.0354 1.843 0 1.913 0 2.976-0.2126 4.287-0.6732 1.169-0.3898 1.913-0.815 2.693-1.559 0.5669-0.5315 0.6024-0.6024 0.5315-0.7441-0.0354-0.0709-0.7441-0.8504-1.594-1.665l-1.488-1.453-0.1772 0.1063c-1.488 0.9567-3.083 1.453-4.677 1.453-0.8858 0-1.488-0.1417-2.197-0.4961-0.6024-0.2835-1.169-0.7441-1.488-1.24-0.248-0.3898-0.5315-1.134-0.5315-1.382 0-0.1417 0.248-0.1772 6.697-0.1772 6.024 0 6.732 0 6.839-0.1063 0.1417-0.1417 0.1772-1.134 0.0354-2.764-0.1772-2.728-0.9567-4.642-2.551-6.307-1.63-1.701-3.472-2.551-6.024-2.728-0.4252 0-0.815-0.0354-1.205 0zm112.1 0c-0.4252 0-5.173 0.4961-5.244 0.5669-0.1063 0.0354-0.0709 19.1 0 19.17 0.0354 0.0354 1.24 0.0354 2.728 0.0354l2.764-0.0354 0.0354-6.094v-6.094l0.2126-0.3898c0.6732-1.276 1.63-2.126 2.657-2.409 0.7441-0.1772 1.843 0.0354 2.693 0.4961 0.2835 0.1417 0.4961 0.248 0.5315 0.2126 0.0354-0.0709 0.815-4.783 0.815-5.102 0-0.1063 0-0.2126-0.0354-0.2126-0.1417-0.1063-1.736-0.2126-2.409-0.1417-1.417 0.1063-2.693 0.6378-3.791 1.524-0.3543 0.248-0.6378 0.4606-0.6732 0.4606v-1.9842h-0.2835zm55.56 0c-1.807 0-3.26 0.3189-4.713 0.9921-2.799 1.346-4.606 3.543-5.102 6.236-0.2835 1.453-0.248 4.606 0.0709 5.882 0.3898 1.417 1.098 2.657 2.232 3.756 1.665 1.594 3.756 2.587 6.094 2.87 0.6732 0.1063 3.047-0.0354 3.72-0.1772 1.878-0.3898 3.543-1.311 4.996-2.622 0.248-0.2126 0.4606-0.4606 0.4606-0.4961 0-0.1417-3.72-2.941-3.898-2.941-0.0709 0-0.2126 0.1063-0.2835 0.1772-0.2126 0.248-0.9567 0.7795-1.417 1.028-0.9567 0.4606-2.268 0.6378-3.366 0.3898-0.8504-0.1772-1.417-0.5669-2.161-1.311-0.5669-0.5315-0.7441-0.7441-1.063-1.346-0.4252-0.9213-0.5315-1.559-0.5315-2.551 0-1.524 0.4961-2.764 1.594-3.827 0.4961-0.5315 0.7795-0.7795 1.276-1.028 0.815-0.3898 1.276-0.4606 2.268-0.4252 1.24 0.0709 2.161 0.4252 3.189 1.311 0.248 0.1772 0.4961 0.3543 0.5315 0.3543 0.1063 0 3.862-2.835 3.862-2.941 0-0.1417-1.098-1.134-1.807-1.594-1.736-1.169-3.65-1.736-5.953-1.736zm-109.3 0c-1.843 0.0709-3.898 0.4252-5.492 1.063-0.815 0.3189-2.268 1.063-2.409 1.24-0.1063 0.1063-0.0354 0.248 0.8858 1.701 0.5669 0.8858 1.134 1.665 1.169 1.665 0.0354 0 0.3189-0.1063 0.6024-0.248 1.276-0.5669 2.941-0.8504 4.748-0.815 1.276 0.0354 1.807 0.1772 2.445 0.6378 0.5315 0.3898 0.7795 0.8504 0.815 1.559 0.0354 0.6732 0.0709 0.7087-0.3898 0.4606-0.4252-0.1772-1.594-0.6024-2.197-0.7441-0.815-0.1772-1.701-0.248-2.657-0.1772-2.587 0.2126-4.181 0.9213-5.386 2.48-1.169 1.488-1.736 3.437-1.559 5.315 0.1417 1.63 0.5669 2.551 1.63 3.614 0.5315 0.5315 0.8504 0.7441 1.417 1.028 0.815 0.4252 1.736 0.7087 2.799 0.8504 0.9921 0.1417 2.87 0.1417 3.472-0.0354 0.6378-0.1772 1.488-0.5315 2.197-0.9213 0.3189-0.1772 0.6024-0.3189 0.6024-0.3189 0.0354 0 0.0709 0.3189 0.1063 0.6732v0.7087h5.527v-6.307c0.0354-4.358 0-6.626-0.0709-7.087-0.3898-3.331-2.197-5.35-5.28-6.094-0.815-0.2126-1.878-0.2835-2.976-0.248zm-57.93 4.571c0.4606 0 0.8858 0.0709 1.134 0.1417 1.488 0.3898 2.551 1.417 2.693 2.693l0.0709 0.4606h-3.898c-2.516 0-3.933 0-3.969-0.0709-0.0709-0.1063 0.0709-0.9213 0.2835-1.346 0.3898-0.7441 1.559-1.559 2.587-1.772 0.2835-0.0709 0.6732-0.1063 1.098-0.1063zm57.19 5.528c0.2835 0 0.5315 0.0354 0.7795 0.0709 1.276 0.1772 2.126 0.5315 2.587 1.134 0.1772 0.248 0.1417 0.3189 0.1417 1.417 0 1.169 0 1.169-0.2126 1.488-0.2835 0.3898-0.815 0.7087-1.453 0.8858-0.3898 0.1417-0.7087 0.2126-1.594 0.248-0.6378 0-1.346-0.0354-1.524-0.0709-1.701-0.3543-2.622-1.169-2.622-2.409-0.0354-0.8858 0.5669-1.736 1.559-2.232 0.7795-0.3189 1.559-0.4961 2.339-0.5315z",
                    fillOpacity: ".7"
                }), Object(a.jsx)("path", {
                    d: "m430.63 21.646-22.07 0.03516h-22.039v9.3906h8.3613c7.5469 0 8.4328 0.03628 8.5391 0.14258 0.10629 0.1 0.10742 2.0898 0.10742 20.76h-4e-3v20.619h10.027l0.0352-20.619c0-15.197 0.0346-20.689 0.10547-20.76 0.071-0.1063 1.4899-0.10742 8.5059-0.10742h8.4316v-4.7129zm-195.12 0.02344v25.48l2e-3 -0.0098v25.439h10.027l0.0352-10.49 0.0351-10.49h9.3906l6.0938 10.49 6.0586 10.49h5.8106c3.5325 0 3.4814-0.03844 4.002-0.07422 0.22612-0.01554 1.749 9.4e-4 1.7383-0.03125-0.01-0.0194-1.346-2.3691-1.7383-3.0547-1.0232-1.7881-2.0741-3.6124-4.5332-7.9668-3.437-5.984-6.2363-10.872-6.2363-10.979 0.0354-0.0709 0.39096-0.24858 0.85156-0.42578 3.543-1.418 5.8454-3.5786 7.1914-6.7676 1.2048-2.871 1.5951-7.0525 0.92187-10.561-1.24-6.799-6.1315-10.343-15.061-10.98-0.67-0.0355-5.7724-0.07031-12.859-0.07031zm48.637 0v25.48l2e-3 -0.0098v25.439h10.027l0.0351-10.49 0.0352-10.49h9.3906l6.0938 10.49 6.0586 10.49h5.8106c3.5325 0 3.4814-0.03844 4.002-0.07422 0.22612-0.01554 1.749 9.4e-4 1.7383-0.03125-0.01-0.0194-1.346-2.3691-1.7383-3.0547-1.0232-1.7881-2.0741-3.6124-4.5332-7.9668-3.437-5.984-6.2363-10.872-6.2363-10.979 0.0354-0.0709 0.39096-0.24858 0.85156-0.42578 3.543-1.418 5.8454-3.5786 7.1914-6.7676 1.2048-2.871 1.5951-7.0525 0.92187-10.561-1.24-6.799-6.1316-10.343-15.061-10.98-0.67001-0.0355-5.7724-0.07031-12.859-0.07031zm72.309 0.02148c-1.6211-0.02656-3.2671 0.07048-4.8086 0.30078-5.312 0.78-9.9192 3.046-13.781 6.873-4.11 4.07-6.4135 8.7522-7.2285 14.74-0.1772 1.453-0.2126 5.5999 0 7.0879 0.426 3.224 1.2059 5.8096 2.5879 8.4316 2.272 4.468 6.2752 8.4722 10.74 10.74 2.834 1.453 5.5975 2.2687 9.1055 2.623l-4e-3 -0.0098c1.24 0.1417 5.2099 0.10689 6.3789-0.07031 2.019-0.2835 3.3298-0.56835 4.9238-1.0645 3.083-1.028 5.7405-2.5146 8.1855-4.6406 0.85-0.709 2.6925-2.5879 3.2949-3.332 3.047-3.753 4.7472-7.8987 5.3496-12.93 0.1771-1.382 0.1788-4.9253 0.0371-6.2363-0.67301-6.092-2.8712-10.803-6.9102-14.949-3.724-3.827-8.0098-6.1309-13.219-7.123-1.435-0.26575-3.0312-0.41484-4.6524-0.44141zm-159.14 0.01758-10.17 25.41c-5.599 13.96-10.17 25.404-10.17 25.439l-2e-3 0.03125h10.736l1.5234-3.8613 1.5234-3.8281h23.24l1.5234 3.8281 1.4883 3.8613h5.3516c4.252 0 5.3496 5.87e-4 5.3496-0.07031 0-0.07-4.5678-11.511-10.131-25.441l-10.129-25.369h-5.0684zm-47.336 0.02539c-1.2669-0.0088-2.5163 0.01704-3.1543 0.08789-4.462 0.531-7.8645 1.7368-11.23 3.9688-1.417 0.921-2.5153 1.8075-3.8613 3.1895-4.146 4.11-6.4139 8.7476-7.1934 14.559-0.2126 1.488-0.2126 5.7052 0 7.1582 0.425 3.224 1.2048 5.7746 2.5508 8.4316 1.275 2.481 3.0471 4.7848 5.2441 6.8398 4.14 3.862 9.0349 5.9878 14.881 6.5547 1.134 0.1063 5.1726 0.03623 6.3066-0.10547 5.42-0.673 9.8833-2.5175 14.029-5.8125 0.4252-0.3189 0.78101-0.63808 0.81641-0.70898 0.035-0.071-6.5556-7.334-6.6973-7.334-0.0355 0-0.24809 0.14116-0.49609 0.31836-3.293 2.516-7.5098 3.7924-12.01 3.6152-3.437-0.107-5.9886-0.88758-8.4336-2.5176-3.402-2.298-5.4577-5.6992-6.1309-10.199-0.1772-1.276-0.1772-4.3583 0-5.5273 0.39-2.374 1.1348-4.2508 2.3398-6.0938 2.8-4.181 7.2664-6.3789 12.9-6.3789 3.897 0 7.5102 1.0636 10.699 3.2246 0.6026 0.4252 1.1342 0.74438 1.2051 0.70898 0.036 0 1.0283-1.0638 2.1973-2.3398 1.169-1.275 2.6571-2.9046 3.2949-3.6133 1.3819-1.4879 1.3813-1.2403 0.0703-2.2324-4.113-3.224-8.6114-5.0321-14.068-5.6699-0.7085-0.07085-1.9929-0.11426-3.2598-0.12305zm205.39 9.3711c3.2231-0.09281 6.411 0.69117 8.8027 2.2324 3.826 2.477 6.3073 6.5178 6.9805 11.301 0.1417 1.169 0.17686 3.685 0.0352 4.748-0.39 2.976-1.3824 5.6325-2.9414 7.6875-2.733 3.685-6.2049 5.6707-10.67 6.0605l4e-3 0.0059c-2.339 0.2126-4.7488-0.03578-6.8398-0.70898-4.606-1.524-8.3256-5.5989-9.6016-10.631-0.4252-1.665-0.53125-2.5153-0.53125-4.5703 0-2.374 0.21205-3.8981 0.81445-5.7051 1.705-5.14 5.7442-8.8972 10.74-10.031 1.0538-0.23025 2.1326-0.35774 3.207-0.38867zm-97.697 0.05664c3.4996 0.0098 3.9439 0.08895 4.8477 0.32812 2.02 0.602 3.2252 1.8408 3.6504 3.7188 0.1772 0.815 0.10518 2.2338-0.10742 3.0488-0.67384 2.3025-2.4823 3.578-5.457 3.791-0.53336 0.07086-4.0743 0.10742-7.9004 0.10742-5.776 0-6.9447-0.03652-7.0156-0.10742-0.0709-0.071-0.10769-1.5942-0.0723-5.4922v-5.3848h7.4062c1.9755-0.0088 3.4819-0.01304 4.6484-0.0098zm48.637 0c3.4996 0.0098 3.9439 0.08895 4.8477 0.32812 2.02 0.602 3.2252 1.8408 3.6504 3.7188 0.1772 0.815 0.10518 2.2338-0.10742 3.0488-0.67384 2.3025-2.4823 3.578-5.457 3.791-0.53337 0.07086-4.0744 0.10742-7.9004 0.10742-5.776 0-6.9447-0.03652-7.0156-0.10742-0.0709-0.071-0.10766-1.5942-0.0723-5.4922v-5.3848h7.4062c1.9755-0.0088 3.4819-0.01301 4.6484-0.0098zm-103.67 4.1914c0.0708 0 0.14258 0.03457 0.14258 0.10547 2.693 6.8 7.3337 18.849 7.3691 18.99v2e-3l0.0371 0.21289h-7.584c-5.209 1e-6 -7.6189-0.03686-7.6543-0.07227-0.071-0.14 7.5832-19.238 7.6894-19.238z",
                    fillOpacity: ".8"
                })]
            }), Object(a.jsx)("rect", {x: "-135.63", y: "-39.638", width: "0", height: "0", fill: "none"})]
        }), h = r(54), m = r(22), p = r(52), b = r(111), g = Object(h.b)() ? {
            product: "Carrot2",
            pageTitle: "Carrot2 search results clustering engine",
            createProductName: () => Object(a.jsxs)(a.Fragment, {children: ["Carrot", Object(a.jsx)("sup", {children: "2"})]}),
            createAppLogo: () => Object(a.jsx)(l, {}),
            createAppInfoNavLink: () => Object(a.jsx)(p.a, {
                icon: b.a,
                title: "Source code on GitHub",
                path: "https://github.com/carrot2/carrot2"
            }),
            createSlogan: () => Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsxs)("a", {
                    href: "http://project.carrot2.org",
                    children: ["Carrot", Object(a.jsx)("sup", {children: "2"})]
                }), " ", "organizes your search results into topics. With an instant overview of what's available, you will quickly find what you're looking for."]
            }),
            createStartPageLogo: () => Object(a.jsxs)(a.Fragment, {children: [Object(a.jsx)(l, {}), Object(a.jsx)(u, {title: "Carrot2"})]}),
            createAboutIntro: () => Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsxs)("p", {
                    children: ["This is the demo application of the", " ", Object(a.jsxs)("a", {
                        href: "http://project.carrot2.org",
                        target: "_blank",
                        rel: "noreferrer",
                        children: ["Carrot", Object(a.jsx)("sup", {children: "2"}), " clustering engine"]
                    }), ". It uses Carrot", Object(a.jsx)("sup", {children: "2"}), "'s algorithms to organize search results into thematic folders."]
                }), Object(a.jsx)("h3", {children: "User interfaces"}), Object(a.jsxs)("ul", {
                    style: {
                        listStyle: "none",
                        paddingLeft: "0"
                    },
                    children: [Object(a.jsxs)("li", {
                        children: [Object(a.jsx)("strong", {
                            children: Object(a.jsxs)(n.c, {
                                to: m.a.searchStart.path,
                                children: [Object(a.jsx)(i.a, {icon: s.v}), "Web Search Clustering"]
                            })
                        }), " ", "organizes search results from public search engines into clusters; offers treemap- and pie-chart visualizations of the clusters."]
                    }), Object(a.jsxs)("li", {
                        children: [Object(a.jsx)("strong", {
                            children: Object(a.jsxs)(n.c, {
                                to: m.a.workbench.path,
                                children: [Object(a.jsx)(i.a, {icon: s.l}), "Clustering Workbench"]
                            })
                        }), " ", "clusters content from local files in JSON or Excel format, Solr or Elasticsearch; allows tuning of clustering parameters and exporting results as Excel or JSON."]
                    })]
                })]
            }),
            createAboutDetails: () => Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)("h3", {children: "FAQ"}), Object(a.jsxs)("dl", {
                    children: [Object(a.jsx)("dt", {children: "Is this application Open Source?"}), Object(a.jsx)("dd", {
                        children: Object(a.jsxs)("p", {
                            children: ["Yes, the source code of this demo application is available as part of the", " ", Object(a.jsxs)("a", {
                                href: "http://project.carrot2.org",
                                children: ["Carrot", Object(a.jsx)("sup", {children: "2"})]
                            }), " ", "framework under the Apache Software License 2.0. This means you can freely reuse this application, along with Carrot", Object(a.jsx)("sup", {children: "2"}), " ", "clustering algorithms, for your open source or commercial projects."]
                        })
                    }), Object(a.jsx)("dt", {children: "What happens to the data I submit for clustering?"}), Object(a.jsx)("dd", {
                        children: Object(a.jsxs)("p", {
                            children: ["The data is sent to Carrot", Object(a.jsx)("sup", {children: "2"}), " Document Clustering Server, located at", " ", Object(a.jsx)("a", {
                                href: Object(h.a)().toString(),
                                target: "_blank",
                                rel: "noreferrer",
                                children: Object(h.a)().toString()
                            }), ", for clustering. The server will keep the data in memory for the duration of the clustering process. None of the data you submit will be permanently stored or logged."]
                        })
                    })]
                }), Object(a.jsx)("h3", {children: "Further reading"}), Object(a.jsxs)("ul", {
                    children: [Object(a.jsxs)("li", {
                        children: ["Source code of this application and several clustering algorithms is available in the", " ", Object(a.jsxs)("a", {
                            href: "http://project.carrot2.org",
                            target: "_blank",
                            rel: "noreferrer",
                            children: ["Carrot", Object(a.jsx)("sup", {children: "2"}), " framework"]
                        }), "."]
                    }), Object(a.jsxs)("li", {
                        children: ["The treemap view uses the", " ", Object(a.jsx)("a", {
                            href: "https://carrotsearch.com/foamtree/",
                            children: "Carrot Search FoamTree"
                        }), " ", "visualization component."]
                    }), Object(a.jsxs)("li", {
                        children: ["The pie-chart view uses the", " ", Object(a.jsx)("a", {
                            href: "https://carrotsearch.com/circles/",
                            children: "Carrot Search Circles"
                        }), " ", "visualization component."]
                    })]
                })]
            }),
            createUnlimitedDistributionInfo: () => Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)("strong", {children: "Note:"}), " If you have IT and programming skills, you can install this application on your own hardware. This will remove limits on the rate and size of clustering requests. Please see", " ", Object(a.jsx)("a", {
                    href: "http://project.carrot2.org",
                    target: "_blank",
                    rel: "noopener noreferrer",
                    children: "http://project.carrot2.org"
                }), " ", "for more details."]
            })
        } : {
            product: "Lingo3G",
            createProductName: () => Object(a.jsx)(a.Fragment, {children: "Lingo3G"}),
            pageTitle: "Carrot2 search results clustering engine",
            createSlogan: () => Object(a.jsxs)(a.Fragment, {
                children: ["This app uses Carrot Search", " ", Object(a.jsx)("a", {
                    href: "https://carrotsearch.com/lingo3g",
                    children: "Lingo3G"
                }), " to organize search results into clearly-labeled topics for instant overview and efficient research."]
            }),
            createStartPageLogo: () => Object(a.jsxs)(a.Fragment, {children: [Object(a.jsx)(l, {}), Object(a.jsx)(d, {title: "Carrot Search"})]}),
            createAboutIntro: () => Object(a.jsx)("div", {children: "TBD"}),
            createAboutDetails: () => Object(a.jsx)("div", {children: "TBD"}),
            createUnlimitedDistributionInfo: () => Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)("strong", {children: "Tip:"}), " If you have IT and programming skills, you can install this application on your own hardware. This will remove limits on the rate and size of clustering requests. Get in touch at", Object(a.jsx)("a", {
                    href: "mailto:info@carrotsearch.com",
                    target: "_blank",
                    rel: "noopener noreferrer",
                    children: "info@carrotsearch.com"
                }), " ", "for an evaluation package."]
            })
        }
}, function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return H
    }));
    var a = r(106), n = r(14), i = r(13), s = r(17), o = r(5), c = {
            algorithms: {
                "Bisecting K-Means": ["Arabic", "Armenian", "Brazilian", "Bulgarian", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek", "Hindi", "Hungarian", "Indonesian", "Irish", "Italian", "Latvian", "Lithuanian", "Norwegian", "Polish", "Portuguese", "Romanian", "Russian", "Spanish", "Swedish", "Thai", "Turkish"],
                Lingo: ["Arabic", "Armenian", "Brazilian", "Bulgarian", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek", "Hindi", "Hungarian", "Indonesian", "Irish", "Italian", "Latvian", "Lithuanian", "Norwegian", "Polish", "Portuguese", "Romanian", "Russian", "Spanish", "Swedish", "Thai", "Turkish"],
                STC: ["Arabic", "Armenian", "Brazilian", "Bulgarian", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician", "German", "Greek", "Hindi", "Hungarian", "Indonesian", "Irish", "Italian", "Latvian", "Lithuanian", "Norwegian", "Polish", "Portuguese", "Romanian", "Russian", "Spanish", "Swedish", "Thai", "Turkish"]
            }
        }, l = (e, t, r) => {
            var a = c.algorithms[t];
            return Object(o.a)({
                id: "".concat(e, ":language"),
                type: "enum",
                ui: "select",
                label: "Language",
                description: "\n<p>\n  The language in which to perform clustering. Set it\n  to the language in which the majority of input documents is written.\n</p>",
                options: a.map((e => ({value: e})))
            }, r)
        }, u = Object(s.f)(a), d = (e, t) => Object(s.g)(u, e, t), h = (e, t, r) => Object(s.h)(u, e, t, r),
        m = (e, t) => Object(s.i)(u, e, t), p = () => v,
        b = [d("desiredClusterCount"), d("preprocessing.documentAssigner.minClusterSize"), ...h("clusterBuilder.labelAssigner", p, (() => ({ui: "radio"}))), d("preprocessing.documentAssigner.exactPhraseAssignment"), Object(s.a)(d("clusterBuilder.clusterMergingThreshold")), Object(s.a)(d("scoreWeight"))],
        g = [d("clusterBuilder.phraseLabelBoost"), Object(s.a)(d("clusterBuilder.phraseLengthPenaltyStart")), Object(s.a)(d("clusterBuilder.phraseLengthPenaltyStop")), ...m("preprocessing.labelFilters.completeLabelFilter", p), ...m("preprocessing.labelFilters.genitiveLabelFilter", p), ...m("preprocessing.labelFilters.minLengthLabelFilter", p), ...m("preprocessing.labelFilters.numericLabelFilter", p), ...m("preprocessing.labelFilters.queryLabelFilter", p), ...m("preprocessing.labelFilters.stopLabelFilter", p), ...m("preprocessing.labelFilters.stopWordLabelFilter", p)],
        j = [...h("matrixBuilder.termWeighting", p), d("matrixBuilder.boostFields"), d("matrixBuilder.boostedFieldWeight"), Object(s.a)(d("preprocessing.phraseDfThreshold")), Object(s.a)(d("preprocessing.wordDfThreshold")), Object(s.a)(d("matrixBuilder.maxWordDf")), ...h("matrixReducer.factorizationFactory", p), d("matrixBuilder.maximumMatrixSize")],
        f = [Object(s.d)("lingo"), Object(s.e)("lingo")],
        x = Object(n.b)("parameters:algorithm:lingo", Object.assign({language: "English"}, Object(s.b)(u, [b, g, j, f])));
    j.unshift(l("lingo", "Lingo", Object(i.e)(x, "language")));
    var v = e => x[e.id], O = [{
            id: "lingo",
            type: "group",
            settings: [{
                id: "lingo:clusters",
                type: "group",
                label: "Clusters",
                settings: b,
                description: "Parameters affecting the number, structure and content of clusters."
            }, {
                id: "lingo:labels",
                type: "group",
                label: "Cluster labels",
                settings: g,
                description: "Customization of cluster labels."
            }, {
                id: "lingo:dictionaries",
                type: "group",
                label: "Dictionaries",
                settings: f,
                description: "Label and word exclusion dictionaries."
            }, {
                id: "lingo:languageModel",
                type: "group",
                label: "Language model",
                settings: j,
                description: "Parameters of the document representation used by the clustering algorithm."
            }],
            get: v,
            set: (e, t) => x[e.id] = t
        }], y = {
            label: "Lingo",
            description: "Well-described flat clusters.",
            descriptionHtml: "creates well-described flat clusters. Does not scale beyond a few thousand search results. Available as part of the open source <a href='http://project.carrot2.org' target='_blank'>Carrot<sup>2</sup> framework</a>.",
            tag: "open source",
            getSettings: () => O,
            getLanguage: () => x.language,
            getDefaults: x.getDefaults,
            resetToDefaults: x.resetToDefaults,
            applyQueryHint: (e, t) => e.queryHint = t
        }, w = r(109), S = Object(s.f)(w), F = (e, t) => Object(s.g)(S, e, t),
        C = [F("maxClusters"), F("maxBaseClusters"), F("minBaseClusterScore"), F("minBaseClusterSize"), F("documentCountBoost"), Object(s.a)(F("mergeStemEquivalentBaseClusters")), Object(s.a)(F("mergeThreshold")), Object(s.a)(F("scoreWeight"))],
        k = [F("singleTermBoost"), F("optimalPhraseLength"), F("optimalPhraseLengthDev"), F("maxWordsPerLabel"), F("maxPhrasesPerLabel"), Object(s.a)(F("maxPhraseOverlap")), Object(s.a)(F("mostGeneralPhraseCoverage"))],
        T = [Object(s.a)(F("ignoreWordIfInHigherDocsPercent", {label: "Max relative word DF"})), Object(s.a)(F("preprocessing.wordDfThreshold"))],
        L = Object(n.b)("parameters:algorithm:stc", Object.assign({language: "English"}, Object(s.b)(S, [C, k, T])));
    T.unshift(l("stc", "STC", Object(i.e)(L, "language")));
    var I = [{
            id: "stc",
            type: "group",
            settings: [{
                id: "stc:clusters",
                type: "group",
                label: "Clusters",
                settings: C,
                description: "Parameters affecting the number, structure and content of clusters."
            }, {
                id: "stc:labels",
                type: "group",
                label: "Cluster labels",
                settings: k,
                description: "Customization of cluster labels."
            }, {
                id: "stc:languageModel",
                type: "group",
                label: "Language model",
                settings: T,
                description: "Parameters of the document representation used by the clustering algorithm."
            }],
            get: e => L[e.id],
            set: (e, t) => L[e.id] = t
        }], z = {
            label: "STC",
            description: "Flat clusters, fast algorithm.",
            descriptionHtml: "the classic search results clustering algorithm. Produces flat cluster with adequate description, very fast. Available as part of the open source <a href='http://project.carrot2.org' target='_blank'>Carrot<sup>2</sup> framework</a>",
            tag: "open source",
            getSettings: () => I,
            getLanguage: () => L.language,
            getDefaults: L.getDefaults,
            resetToDefaults: L.resetToDefaults,
            applyQueryHint: (e, t) => e.queryHint = t
        }, q = r(110), N = Object(s.f)(q), R = (e, t) => Object(s.g)(N, e, t), D = (e, t, r) => Object(s.h)(N, e, t, r),
        P = () => W, M = [R("clusterCount"), R("maxIterations"), R("partitionCount")], E = [R("labelCount")],
        A = [...D("matrixBuilder.termWeighting", P), R("matrixBuilder.boostFields"), R("matrixBuilder.boostedFieldWeight"), Object(s.a)(R("matrixBuilder.maxWordDf")), Object(s.a)(R("preprocessing.wordDfThreshold")), R("useDimensionalityReduction"), ...D("matrixReducer.factorizationFactory", P), R("matrixBuilder.maximumMatrixSize")],
        B = Object(n.b)("parameters:algorithm:kmeans", Object.assign({language: "English"}, Object(s.b)(N, [M, E, A])));
    A.unshift(l("kmeans", "Bisecting K-Means", Object(i.e)(B, "language")));
    var W = e => B[e.id], J = [{
        id: "kmeans",
        type: "group",
        settings: [{
            id: "kmeans:clusters",
            type: "group",
            label: "Clusters",
            settings: M,
            description: "Parameters affecting the number, structure and content of clusters."
        }, {
            id: "kmeans:labels",
            type: "group",
            label: "Cluster labels",
            settings: E,
            description: "Customization of cluster labels."
        }, {
            id: "kmeans:languageModel",
            type: "group",
            label: "Language model",
            settings: A,
            description: "Parameters of the document representation used by the clustering algorithm."
        }],
        get: W,
        set: (e, t) => B[e.id] = t
    }], H = {
        Lingo: y,
        STC: z,
        "Bisecting K-Means": {
            label: "k-means",
            description: "Base line algorithm, bag-of-words labels.",
            descriptionHtml: "base line clustering algorithm, produces bag-of-words style cluster descriptions. Available as part of the open source <a href='http://project.carrot2.org' target='_blank'>Carrot<sup>2</sup> framework</a>",
            tag: "open source",
            getSettings: () => J,
            getLanguage: () => B.language,
            getDefaults: B.getDefaults,
            resetToDefaults: B.resetToDefaults,
            applyQueryHint: (e, t) => e.queryHint = t
        }
    }
}, , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return o
    })), r.d(t, "c", (function () {
        return c
    })), r.d(t, "b", (function () {
        return u
    })), r.d(t, "d", (function () {
        return b
    }));
    var a = r(0), n = (r(213), r(1), r(28)), i = ({children: e}) => Object(a.jsxs)("div", {
            className: "Error",
            children: [e, Object(a.jsx)("p", {children: "That's all we know, sorry."})]
        }), s = ({error: e, children: t}) => {
            var r, n;
            e instanceof Error ? r = "".concat(e.name, ": ").concat(e.message) : r = null === e || void 0 === e || null === (n = e.statusText) || void 0 === n ? void 0 : n.replace(/([&/?])/g, "$1\u200b");
            return Object(a.jsxs)(i, {error: e, children: [t, Object(a.jsx)("pre", {children: r})]})
        }, o = ({error: e}) => Object(a.jsxs)(s, {
            error: e,
            children: [Object(a.jsx)("h2", {children: "Search engine error"}), Object(a.jsx)("p", {children: "Search could not be performed due to the following error:"})]
        }),
        c = ({children: e}) => Object(a.jsxs)(i, {children: [Object(a.jsx)("h2", {children: "Search engine error"}), Object(a.jsx)("p", {children: "Search could not be performed due to the following error:"}), e]}),
        l = ({response: e}) => e ? Object(a.jsxs)("dl", {
            className: "ResponseInfo",
            children: [Object(a.jsx)("dt", {children: "URL"}), Object(a.jsx)("dd", {children: e.url}), Object(a.jsx)("dt", {children: "Status"}), Object(a.jsxs)("dd", {children: [e.status, " ", e.statusText]})]
        }) : null, u = ({
                            error: e,
                            children: t
                        }) => Object(a.jsxs)(a.Fragment, {children: [t, Object(a.jsx)(l, {response: e.response})]}),
        d = () => Object(a.jsxs)("div", {
            className: "Error",
            children: [Object(a.jsx)("h2", {children: "Too many clustering requests"}), Object(a.jsx)("p", {children: "You are making too many clustering requests for our little demo server to handle. Please check back in a minute."}), Object(a.jsx)("p", {
                children: Object(a.jsx)("small", {
                    className: "light",
                    children: n.a.createUnlimitedDistributionInfo()
                })
            })]
        }), h = () => Object(a.jsxs)("div", {
            className: "Error",
            children: [Object(a.jsx)("h2", {children: "Too much data to cluster"}), Object(a.jsx)("p", {children: "You sent too much data for our little demo server to handle. Lower the number of search results and try again."}), Object(a.jsx)("p", {
                children: Object(a.jsx)("small", {
                    className: "light",
                    children: n.a.createUnlimitedDistributionInfo()
                })
            })]
        }), m = ({exception: e}) => Object(a.jsxs)("div", {
            className: "Error",
            children: [Object(a.jsx)("h2", {children: "Clustering engine error"}), Object(a.jsx)("p", {children: "Results could not be clustered due to the following error:"}), Object(a.jsx)("pre", {children: e.stacktrace}), Object(a.jsx)("p", {children: "That's all we know."})]
        }),
        p = ({message: e}) => Object(a.jsxs)(i, {children: [Object(a.jsx)("h2", {children: "Clustering engine error"}), Object(a.jsx)("p", {children: "Results could not be clustered due to the following error:"}), Object(a.jsx)("pre", {children: e})]}),
        b = e => {
            if (e && 429 === e.status) return Object(a.jsx)(d, {});
            if (e && 413 === e.status) return Object(a.jsx)(h, {});
            if (e && e.bodyParsed) {
                if (e.bodyParsed.stacktrace) return Object(a.jsx)(m, {exception: e.bodyParsed});
                if (e.bodyParsed.message) return Object(a.jsx)(p, {message: e.bodyParsed.message})
            }
            return Object(a.jsxs)(s, {
                error: e,
                children: [Object(a.jsx)("h2", {children: "Clustering engine error"}), Object(a.jsx)("p", {children: "Results could not be clustered due to the following error:"})]
            })
        }
}, , , , , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return c
    }));
    var a = r(5), n = r(26), i = r(0), s = (r(1), r(211), r(6)), o = r.n(s), c = e => {
        var t = e.className, r = void 0 === t ? "" : t, s = e.children, c = e.enabled, l = void 0 === c || c,
            u = Object(n.a)(e, ["className", "children", "enabled"]);
        return Object(i.jsx)("button", Object(a.a)(Object(a.a)({}, u), {}, {
            disabled: !l,
            className: o()("link", r),
            children: s
        }))
    }
}, , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return o
    })), r.d(t, "b", (function () {
        return c
    })), r.d(t, "c", (function () {
        return l
    }));
    var a = r(27), n = r(4), i = r(12), s = () => {
        var e = Object(n.d)({
            selected: new Set, toggleSelection: function (t, r) {
                var a = e.selected;
                if (!r) {
                    if (1 === a.size && a.has(t)) return void a.delete(t);
                    e.clear()
                }
                e.isSelected(t) ? a.delete(t) : a.add(t)
            }, replaceSelection: function (t) {
                for (var r = new Set(t), a = e.selected, n = 0, i = Array.from(a.values()); n < i.length; n++) {
                    var s = i[n];
                    r.has(s) || a.delete(s)
                }
                t.forEach((e => {
                    a.add(e)
                }))
            }, isSelected: function (t) {
                return e.selected.has(t)
            }, clear: function () {
                var t, r = e.selected, n = Object(a.a)(r.values());
                try {
                    for (n.s(); !(t = n.n()).done;) {
                        var i = t.value;
                        r.delete(i)
                    }
                } catch (s) {
                    n.e(s)
                } finally {
                    n.f()
                }
            }
        });
        return e
    }, o = s(), c = s(), l = Object(n.d)({
        allDocumentsVisible: !0, visibleDocumentIds: new Set, isVisible: function (e) {
            return l.visibleDocumentIds.has(e.__id)
        }, replaceVisible: function (e) {
            var t, r = l.visibleDocumentIds, n = Object(a.a)(r);
            try {
                for (n.s(); !(t = n.n()).done;) {
                    var i = t.value;
                    e.has(i) || r.delete(i)
                }
            } catch (u) {
                n.e(u)
            } finally {
                n.f()
            }
            var s, o = Object(a.a)(e);
            try {
                for (o.s(); !(s = o.n()).done;) {
                    var c = s.value;
                    r.add(c)
                }
            } catch (u) {
                o.e(u)
            } finally {
                o.f()
            }
            l.allDocumentsVisible = 0 === r.size
        }
    });
    Object(n.a)((function () {
        var e = new Set;
        !function e(t, r) {
            if (t) {
                var n, i = Object(a.a)(t);
                try {
                    for (i.s(); !(n = i.n()).done;) {
                        var s, o = n.value, c = Object(a.a)(o.documents);
                        try {
                            for (c.s(); !(s = c.n()).done;) {
                                var l = s.value;
                                r.add(l)
                            }
                        } catch (u) {
                            c.e(u)
                        } finally {
                            c.f()
                        }
                        e(o.clusters, r)
                    }
                } catch (u) {
                    i.e(u)
                } finally {
                    i.f()
                }
            }
        }(o.selected, e);
        var t, r = Object(a.a)(c.selected);
        try {
            for (r.s(); !(t = r.n()).done;) {
                var n = t.value;
                e.add(n.__id)
            }
        } catch (i) {
            r.e(i)
        } finally {
            r.f()
        }
        l.replaceVisible(e)
    }));
    var u = void 0;
    Object(n.a)((function () {
        i.d.clusters !== u && (o.clear(), u = i.d.clusters)
    }))
}, function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return d
    }));
    var a = r(5), n = r(26), i = r(0), s = (r(1), r(175), r(6)), o = r.n(s), c = r(23), l = r(40), u = r(45), d = e => {
        var t = e.children, r = e.position, s = void 0 === r ? c.a.BOTTOM_RIGHT : r, d = e.popoverClassName,
            h = Object(n.a)(e, ["children", "position", "popoverClassName"]), m = Object(u.c)(t);
        return Object(i.jsxs)(l.h, Object(a.a)(Object(a.a)({
            position: s,
            autoFocus: !0,
            popoverClassName: o()("ToolPopover", d),
            boundary: "viewport"
        }, h), {}, {children: [m[0], m[1]]}))
    }
}, function (e, t, r) {
    "use strict";

    function a(e, t) {
        var r = e.toFixed(t - 1);
        return r.substring(0, Math.max(r.indexOf("."), t + 1)).replace(/\.(\d*?)(0)+$/, ".$1").replace(/\.$/, "")
    }

    r.d(t, "b", (function () {
        return n
    })), r.d(t, "c", (function () {
        return i
    })), r.d(t, "a", (function () {
        return s
    }));
    var n = function (e) {
        if (null === e || void 0 === e) return e;
        if (isNaN(e) || !isFinite(e)) return e;
        if (e < 1e3) return e + "ms";
        if (e < 6e4) return a(e / 1e3, 3) + "s";
        var t = Math.floor(e / 6e4), r = Math.round((e - 60 * t * 1e3) / 1e3);
        return t + "m" + (r > 0 ? " " + r + "s" : "")
    };

    function i(e, t, r = !0) {
        return (r ? e + " " : " ") + t + (1 !== e ? "s" : "")
    }

    function s(e) {
        return e + (e.endsWith(".") ? "" : ".")
    }
}, function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return a
    })), r.d(t, "b", (function () {
        return n
    })), r.d(t, "c", (function () {
        return i
    })), r.d(t, "d", (function () {
        return s
    }));
    var a = e => {
        var t = Object.keys(e);
        return t.length > 0 ? e[t[0]] : void 0
    }, n = (e, t) => {
        for (var r in e) e.hasOwnProperty(r) && t(e[r], r)
    }, i = (e, t, r) => {
        e.has(t) ? e.set(t, e.get(t) + r) : e.set(t, r)
    }, s = e => void 0 === e || null === e || "string" === typeof e && "" === e
}, function (e, t, r) {
    "use strict";
    r.d(t, "b", (function () {
        return a
    })), r.d(t, "c", (function () {
        return n
    })), r.d(t, "a", (function () {
        return i
    }));
    var a = (e, t, r, a = (e => e)) => {
            if (0 !== t) {
                var n = 0;
                return e.map(((e, i) => {
                    var s;
                    if (n + 80 >= t) return null;
                    var o = a(e);
                    return o ? (s = n + o.length < t ? o : o.substring(0, t - n) + "\u2026", n += s.length, r(s, e, i)) : (console.log("null", e), null)
                })).filter((e => null !== e))
            }
        }, n = e => Array.isArray(e) ? e : [e],
        i = (e, t) => Array.isArray(e) && Array.isArray(t) && e.length === t.length && e.every(((e, r) => e === t[r]))
}, , , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return j
    }));
    var a = r(26), n = r(21), i = r(0), s = r(1), o = r(6), c = r.n(o), l = r(15), u = r(2), d = r(40), h = r(64),
        m = (r(206), r(42)), p = e => Object(i.jsx)("span", {
            className: e.className,
            title: e.title,
            style: e.visible ? {} : {display: "none"},
            children: e.children
        }), b = ({tool: e, visible: t, props: r}) => e.icon ? Object(i.jsxs)(m.a, {
            className: u.a.FIXED,
            disabled: !t,
            position: e.position,
            children: [Object(i.jsx)(p, {
                visible: t,
                className: "view-tool-trigger",
                children: Object(i.jsx)(d.a, {icon: Object(i.jsx)(l.a, {icon: e.icon}), minimal: !0, title: e.title})
            }), e.createContentElement(r)]
        }) : Object(i.jsx)(p, {
            visible: t,
            className: u.a.FIXED + " view-tool-trigger",
            title: e.title,
            children: e.createContentElement(r)
        }), g = e => {
            var t = Object(s.useState)(!1), r = Object(n.a)(t, 2), a = r[0], o = r[1];
            return Object(s.useEffect)((() => {
                e.visible && o(!0)
            }), [e.visible]), a ? Object(i.jsx)("div", {
                style: {
                    display: e.visible ? "block" : "none",
                    position: "relative"
                }, children: e.createElement(e.visible, e.props)
            }) : null
        }, j = e => {
            var t = e.views, r = e.className, n = e.activeView, s = e.onViewChange, o = e.children,
                l = Object(a.a)(e, ["views", "className", "activeView", "onViewChange", "children"]),
                u = (e => e.reduce(((e, t) => (Object.assign(e, t.views), e)), {}))(t), m = Object.keys(u);
            return Object(i.jsxs)("div", {
                className: c()("Views", r),
                children: [Object(i.jsxs)(d.c, {
                    className: "ViewsTabs",
                    fill: !0,
                    vertical: !1,
                    children: [Object(i.jsx)(h.a, {
                        selectedTabId: n, onChange: s, children: t.map((e => {
                            var t = [];
                            return e.label && t.push(Object(i.jsx)("div", {
                                className: "TabGroupLabel",
                                children: e.label
                            }, e.label)), t.concat(Object.keys(e.views).map((e => Object(i.jsx)(d.o, {
                                id: e,
                                title: u[e].label
                            }, e))))
                        }))
                    }), m.filter((e => u[e].tools && u[e].tools.length > 0)).reduce((function (e, t) {
                        return u[t].tools.forEach((r => {
                            var a = t + "." + r.id;
                            e.push(Object(i.jsx)(b, {tool: r, visible: n === t, props: l}, a))
                        })), e
                    }), [])]
                }), Object(i.jsxs)("div", {
                    className: "ViewsContent",
                    children: [o, m.map((e => Object(i.jsx)(g, {
                        visible: e === n,
                        createElement: u[e].createContentElement,
                        props: l
                    }, e)))]
                })]
            })
        }
}, function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return n
    }));
    var a = r(4), n = Object(a.d)({
        current: null, last: null, addError: e => {
            n.current = e
        }, dismiss: () => {
            n.last = n.current, n.current = null
        }
    })
}, , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return y
    })), r.d(t, "b", (function () {
        return F
    }));
    var a = r(21), n = r(0), i = r(1), s = r.n(i), o = (r(166), r(6)), c = r.n(o), l = r(4), u = r(20), d = r(31),
        h = r(40), m = r(11), p = r(15), b = r(50), g = r(82), j = r(42),
        f = ({to: e, title: t, children: r, icon: s}) => {
            var o = Object(i.useState)(!1), c = Object(a.a)(o, 2), l = c[0], h = c[1], m = Object(u.h)(e);
            return Object(n.jsx)(d.c, {
                onClick: () => h(!1),
                className: "NavLink AppLink",
                to: e,
                activeClassName: "active",
                children: Object(n.jsx)(v, {
                    icon: s,
                    title: t,
                    open: l,
                    onTooltipInteraction: e => h(e && !m),
                    children: r
                })
            })
        }, x = ({href: e, title: t, icon: r, children: s}) => {
            var o = Object(i.useState)(!1), c = Object(a.a)(o, 2), l = c[0], u = c[1];
            return Object(n.jsx)("a", {
                className: "NavLink",
                href: e,
                target: "_blank",
                rel: "noopener noreferrer",
                children: Object(n.jsx)(v, {icon: r, title: t, open: l, onTooltipInteraction: e => u(e), children: s})
            })
        }, v = ({
                    icon: e,
                    title: t,
                    children: r,
                    open: a,
                    onTooltipInteraction: i
                }) => Object(n.jsxs)(j.a, {
            position: h.j.RIGHT,
            interactionKind: h.i.HOVER,
            onInteraction: e => {
                i(e)
            },
            hoverOpenDelay: 450,
            isOpen: a,
            popoverClassName: "NavPopover",
            children: [s.a.isValidElement(e) ? e : Object(n.jsx)(p.a, {
                icon: e,
                size: "2x"
            }), Object(n.jsxs)("div", {children: [Object(n.jsx)("h3", {children: t}), r]})]
        }), O = ({logo: e, apps: t, extras: r, containerClassName: a, children: i}) => {
            var s = [t, r].reduce(((e, t) => {
                    var r;
                    return (null === t || void 0 === t || null === (r = t.props) || void 0 === r ? void 0 : r.children) && (Array.isArray(t.props.children) ? t.props.children.forEach((t => e.push(t))) : e.push(t.props.children)), e
                }), []).filter((e => !!e.props.component)), o = s.find((e => e.props.default)) || s[0], l = Object(u.g)(),
                h = null === a || void 0 === a ? void 0 : a(l);
            return Object(n.jsxs)("div", {
                className: c()("AppContainer", h),
                children: [i, Object(n.jsxs)("nav", {
                    children: [Object(n.jsx)(d.b, {
                        to: "/",
                        children: e
                    }), t, Object(n.jsxs)("div", {className: "NavExtras", children: [r, Object(n.jsx)(g.a, {})]})]
                }), Object(n.jsxs)("main", {
                    children: [Object(n.jsx)(d.a, {
                        children: Object(n.jsxs)(u.d, {
                            children: [Object(n.jsx)(u.a, {
                                from: "/",
                                to: o.props.path,
                                exact: !0
                            }), s.map((e => Object(n.jsx)(u.b, {
                                path: e.props.path,
                                component: e.props.component
                            }, e.props.path))), Object(n.jsx)(u.a, {to: o.props.path})]
                        })
                    }), Object(n.jsx)(S, {})]
                })]
            })
        }, y = ({path: e, component: t, icon: r, title: a, children: i}) => t ? Object(n.jsx)(f, {
            to: e,
            title: a,
            icon: r,
            children: i
        }) : Object(n.jsx)(x, {href: e, icon: r, title: a, children: i}), w = ({children: e}) => e ? Object(n.jsxs)("div", {
            children: [Object(n.jsx)(p.a, {
                icon: m.n,
                size: "2x"
            }), e, Object(n.jsx)("div", {
                className: "AppErrorButtons",
                children: Object(n.jsx)(h.a, {outlined: !1, onClick: () => b.a.dismiss(), children: "Dismiss"})
            })]
        }) : null, S = Object(l.e)((() => {
            var e = b.a.current;
            return Object(i.useEffect)((() => {
                var e = e => {
                    b.a.current && 27 === e.keyCode && b.a.dismiss()
                };
                return window.addEventListener("keyup", e), () => {
                    window.removeEventListener("keyup", e)
                }
            }), []), Object(n.jsx)("div", {
                className: c()("AppError", {visible: null !== e}),
                children: Object(n.jsx)(w, {children: e})
            })
        })), F = ({containerClassName: e, children: t}) => {
            var r = t[0], a = t[1], i = t[2], s = t[3];
            return Object(n.jsx)(d.a, {
                children: Object(n.jsx)(u.d, {
                    children: Object(n.jsx)(u.b, {
                        path: "/",
                        children: Object(n.jsx)(O, {containerClassName: e, logo: r, apps: a, extras: i, children: s})
                    })
                })
            })
        }
}, , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return a
    })), r.d(t, "b", (function () {
        return n
    }));
    var a = () => new URL("/service/cluster?template=frontend-default&serviceInfo", window.location), n = () => !0
}, , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return n
    }));
    var a = r(14), n = Object(a.b)("workbench:ui", {clusterView: "folders"})
}, , , , , , , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return l
    }));
    var a = r(5), n = r(26), i = r(0), s = (r(1), r(40)), o = r(6), c = r.n(o), l = (r(205), e => {
        var t = e.children, r = Object(n.a)(e, ["children"]);
        return Object(i.jsx)(s.p, Object(a.a)(Object(a.a)({}, r), {}, {
            className: c()("PointedTabs", r.className),
            children: t
        }))
    })
}, function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return o
    }));
    var a = r(21), n = r(0), i = r(1), s = r(40), o = ({description: e, children: t}) => {
        var r = Object(i.useState)(!1), o = Object(a.a)(r, 2), l = o[0], u = o[1];
        return Object(i.useEffect)((() => {
            var e = e => {
                27 === e.keyCode && u(!1)
            };
            return document.body.addEventListener("keydown", e), () => {
                document.body.removeEventListener("keydown", e)
            }
        }), []), Object(n.jsx)(s.h, {
            content: Object(n.jsx)(c, {description: e}),
            position: s.j.RIGHT_BOTTOM,
            canEscapeKeyClose: !0,
            isOpen: l,
            onInteraction: u,
            boundary: "viewport",
            children: t
        })
    }, c = ({description: e}) => "string" === typeof e ? Object(n.jsx)("div", {
        className: "SettingDescription",
        dangerouslySetInnerHTML: {__html: e}
    }) : Object(n.jsx)("div", {className: "SettingDescription", children: e})
}, function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return g
    }));
    var a = r(5), n = r(7), i = r.n(n), s = r(16), o = r(21), c = r(0), l = r(1), u = r(40), d = r(2), h = r(15),
        m = r(11), p = r(108), b = r.n(p),
        g = ({contentProvider: e, buttonText: t = "Copy to clipboard", buttonProps: r = {small: !0, minimal: !0}}) => {
            var n, p = Object(l.useState)("none"), g = Object(o.a)(p, 2), j = g[0], f = g[1], x = Object(l.useRef)(),
                v = function () {
                    var t = Object(s.a)(i.a.mark((function t() {
                        var r, a;
                        return i.a.wrap((function (t) {
                            for (; ;) switch (t.prev = t.next) {
                                case 0:
                                    return r = e(), t.prev = 1, t.next = 4, b()(r);
                                case 4:
                                    a = !0, t.next = 10;
                                    break;
                                case 7:
                                    t.prev = 7, t.t0 = t.catch(1), a = !1;
                                case 10:
                                    f(a ? "success" : "error"), x.current && clearTimeout(x.current), x.current = setTimeout((() => {
                                        f("none"), x.current = void 0
                                    }), 1e3);
                                case 13:
                                case"end":
                                    return t.stop()
                            }
                        }), t, null, [[1, 7]])
                    })));
                    return function () {
                        return t.apply(this, arguments)
                    }
                }();
            switch (j) {
                case"success":
                    n = {icon: Object(c.jsx)(h.a, {icon: m.e}), intent: "success", text: "Copied"};
                    break;
                case"error":
                    n = {icon: Object(c.jsx)(h.a, {icon: m.h}), intent: "error", text: "Couldn't copy"};
                    break;
                default:
                    n = {icon: Object(c.jsx)(h.a, {icon: m.d}), text: t, title: "Copy to clipboard"}
            }
            return Object(c.jsx)(u.a, Object(a.a)(Object(a.a)(Object(a.a)({}, n), r), {}, {
                className: d.a.FIXED + " CopyToClipboard",
                onClick: v
            }))
        }
}, , , , , , , , , , , , , , , , function (e, t, r) {
    "use strict";
    r.d(t, "b", (function () {
        return c
    })), r.d(t, "a", (function () {
        return l
    }));
    var a = r(0), n = r(1), i = r(4);
    r(171);

    function s(e) {
        return Object(a.jsxs)("div", {
            className: "LightDarkSwitch ".concat(e.className),
            children: [Object(a.jsx)("input", {
                className: "tgl tgl-ios",
                id: "theme",
                type: "checkbox",
                tabIndex: "0",
                checked: e.dark,
                onChange: e.onChange
            }), Object(a.jsx)("label", {
                className: "tgl-btn",
                htmlFor: "theme",
                title: "Switch to ".concat(e.dark ? "light" : "dark", " theme")
            })]
        })
    }

    var o = r(14),
        c = Object(o.b)("uiConfig", {theme: window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"}, {
            flipTheme: () => c.theme = c.isDarkTheme() ? "light" : "dark",
            isDarkTheme: () => "dark" === c.theme
        }), l = Object(i.e)((() => {
            var e = () => {
                var e = document.body.classList;
                c.isDarkTheme() ? (e.remove("light"), e.add("bp3-dark", "dark")) : (e.remove("bp3-dark", "dark"), e.add("light"))
            };
            Object(n.useEffect)((function () {
                e()
            }), []);
            var t = c.isDarkTheme();
            return Object(a.jsx)(s, {
                className: "ThemeSwitch", dark: t, onChange: () => {
                    c.flipTheme(), e()
                }
            })
        }))
}, , , , , , , , , , , , , , , , , , function (e, t, r) {
}, , , , , , function (e) {
    e.exports = JSON.parse('{"name":"Lingo","type":"org.carrot2.clustering.lingo.LingoClusteringAlgorithm","javadoc":{"text":"Lingo clustering algorithm. Implementation as described in: Stanis\u0142aw Osi\u0144ski, Dawid Weiss: A\\n Concept-Driven Algorithm for Clustering Search Results. IEEE Intelligent Systems, May/June, 3\\n (vol. 20), 2005, pp. 48\u201454.","summary":"Lingo clustering algorithm."},"attributes":{"clusterBuilder":{"id":"clusterBuilder","description":"Cluster label supplier","type":"org.carrot2.clustering.lingo.ClusterBuilder","value":"ClusterBuilder","pathJava":"algorithmInstance.clusterBuilder","pathRest":"clusterBuilder","javadoc":{"text":"Configuration of the structure and labels of clusters.","summary":"Configuration of the structure and labels of clusters."},"implementations":{"ClusterBuilder":{"name":"ClusterBuilder","type":"org.carrot2.clustering.lingo.ClusterBuilder","javadoc":{"text":"Builds cluster labels based on the reduced term-document matrix and assigns documents to the\\n labels.","summary":"Builds cluster labels based on the reduced term-document matrix and assigns documents to the\\n labels."},"attributes":{"clusterMergingThreshold":{"id":"clusterBuilder.clusterMergingThreshold","description":"Cluster merging threshold","type":"Double","value":0.7,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.clusterBuilder.clusterMergingThreshold","pathRest":"clusterBuilder.clusterMergingThreshold","javadoc":{"text":"Percentage of overlap between two cluster\'s document sets at which to merge the clusters. Low\\n values will result in more aggressive merging, which may lead to irrelevant documents in\\n clusters. High values will result in fewer clusters being merged, which may lead to very\\n similar or duplicated clusters.","summary":"Percentage of overlap between two cluster\'s document sets at which to merge the clusters."}},"labelAssigner":{"id":"clusterBuilder.labelAssigner","description":"Cluster label assignment method","type":"org.carrot2.clustering.lingo.LabelAssigner","value":"UniqueLabelAssigner","pathJava":"algorithmInstance.clusterBuilder.labelAssigner","pathRest":"clusterBuilder.labelAssigner","javadoc":{"text":"The method of assigning documents to labels when forming clusters.","summary":"The method of assigning documents to labels when forming clusters."},"implementations":{"SimpleLabelAssigner":{"name":"SimpleLabelAssigner","type":"org.carrot2.clustering.lingo.SimpleLabelAssigner","javadoc":{"text":"A simple and fast label assigner. For each base vector chooses the label that maximizes the base\\n vector--label term vector cosine similarity. Different vectors can get the same label assigned,\\n which means the number of final labels (after duplicate removal) may be smaller than the number\\n of base vectors on input.","summary":"A simple and fast label assigner."},"attributes":{}},"UniqueLabelAssigner":{"name":"UniqueLabelAssigner","type":"org.carrot2.clustering.lingo.UniqueLabelAssigner","javadoc":{"text":"Assigns unique labels to each base vector using a greedy algorithm. For each base vector chooses\\n the label that maximizes the base vector--label term vector cosine similarity and has not been\\n previously selected. Once a label is selected, it will not be used to label any other vector.\\n This algorithm does not create duplicate cluster labels, which usually means that this assignment\\n method will create more clusters than <code>org.carrot2.clustering.lingo.SimpleLabelAssigner</code>. This method is slightly slower\\n than <code>org.carrot2.clustering.lingo.SimpleLabelAssigner</code>.","summary":"Assigns unique labels to each base vector using a greedy algorithm."},"attributes":{}}}},"phraseLabelBoost":{"id":"clusterBuilder.phraseLabelBoost","description":"Phrase label boost","type":"Double","value":1.5,"constraints":["value >= 0.0","value <= 10.0"],"pathJava":"algorithmInstance.clusterBuilder.phraseLabelBoost","pathRest":"clusterBuilder.phraseLabelBoost","javadoc":{"text":"Weight of multi-word labels relative to one-word labels. Low values will result in more\\n one-word labels being produced, higher values will favor multi-word labels.","summary":"Weight of multi-word labels relative to one-word labels."}},"phraseLengthPenaltyStart":{"id":"clusterBuilder.phraseLengthPenaltyStart","description":"Phrase length penalty start","type":"Integer","value":8,"constraints":["value >= 2","value <= 8"],"pathJava":"algorithmInstance.clusterBuilder.phraseLengthPenaltyStart","pathRest":"clusterBuilder.phraseLengthPenaltyStart","javadoc":{"text":"Phrase length at which the overlong multi-word labels should start to be penalized. Phrases of\\n length smaller than <code>phraseLengthPenaltyStart</code> will not be penalized.","summary":"Phrase length at which the overlong multi-word labels should start to be penalized."}},"phraseLengthPenaltyStop":{"id":"clusterBuilder.phraseLengthPenaltyStop","description":"Phrase length penalty stop","type":"Integer","value":8,"constraints":["value >= 2","value <= 8"],"pathJava":"algorithmInstance.clusterBuilder.phraseLengthPenaltyStop","pathRest":"clusterBuilder.phraseLengthPenaltyStop","javadoc":{"text":"Phrase length at which the overlong multi-word labels should be removed completely. Phrases of\\n length larger than <code>phraseLengthPenaltyStop</code> will be removed.","summary":"Phrase length at which the overlong multi-word labels should be removed completely."}}}}}},"desiredClusterCount":{"id":"desiredClusterCount","description":"Desired cluster count","type":"Integer","value":30,"constraints":["value >= 2","value <= 100"],"pathJava":"algorithmInstance.desiredClusterCount","pathRest":"desiredClusterCount","javadoc":{"text":"Determines number of clusters to create. The larger the value, the more clusters will be\\n created. The number of clusters created by the algorithm will be proportional to the value of\\n this parameter, but may be different.","summary":"Determines number of clusters to create."}},"dictionaries":{"id":"dictionaries","description":"Per-request overrides of language components","type":"org.carrot2.language.EphemeralDictionaries","value":"EphemeralDictionaries","pathJava":"algorithmInstance.dictionaries","pathRest":"dictionaries","javadoc":{"text":"Per-request overrides of language components (dictionaries).","summary":"Per-request overrides of language components (dictionaries)."},"implementations":{"EphemeralDictionaries":{"name":"EphemeralDictionaries","type":"org.carrot2.language.EphemeralDictionaries","javadoc":{"text":"Ephemeral per-request overrides for the default <code>org.carrot2.language.LanguageComponents</code> passed to the\\n algorithm.","summary":"Ephemeral per-request overrides for the default <code>org.carrot2.language.LanguageComponents</code> passed to the\\n algorithm."},"attributes":{"labelFilters":{"id":"dictionaries.labelFilters","description":"Cluster label filtering dictionaries.","type":"org.carrot2.language.LabelFilterDictionary[]","value":[],"pathJava":"algorithmInstance.dictionaries.labelFilters","pathRest":"dictionaries.labelFilters","javadoc":{"text":"Additional label filtering dictionaries (supplying cluster label filters that should be\\n discarded from the output).\\n\\n <p>One or more dictionaries can be supplied. The default implementation in <code>org.carrot2.language.DefaultDictionaryImpl</code> supports exact string matching and regular expression patterns.\\n\\n <p>REST-style example using the default implementation:\\n\\n <pre><code>&quot;labelFilters&quot;: [{\\n   &quot;exact&quot;: [&quot;Cluster Label 1&quot;, &quot;Foo Bar&quot;],\\n   &quot;regexp&quot;: [\\n     &quot;(?).+pattern1.+&quot;,\\n     &quot;(?).+[0-9]{2}.+&quot;\\n   ]\\n }]</code></pre>","summary":"Additional label filtering dictionaries (supplying cluster label filters that should be\\n discarded from the output)."}},"wordFilters":{"id":"dictionaries.wordFilters","description":"Word filtering dictionaries.","type":"org.carrot2.language.StopwordFilterDictionary[]","value":[],"pathJava":"algorithmInstance.dictionaries.wordFilters","pathRest":"dictionaries.wordFilters","javadoc":{"text":"Additional stop word filtering dictionaries (supplying word filters that should be discarded\\n from the input).\\n\\n <p>One or more dictionaries can be supplied. The default implementation in <code>org.carrot2.language.DefaultDictionaryImpl</code> supports exact string matching and regular expression patterns.\\n\\n <p>REST-style example using the default implementation:\\n\\n <pre><code>&quot;wordFilters&quot;: [{\\n   &quot;exact&quot;: [&quot;word1&quot;, &quot;word2&quot;],\\n   &quot;regexp&quot;: [\\n     &quot;(?).+pattern1.+&quot;,\\n     &quot;(?).+[0-9]{2}.+&quot;\\n   ]\\n }]</code></pre>","summary":"Additional stop word filtering dictionaries (supplying word filters that should be discarded\\n from the input)."}}}}}},"matrixBuilder":{"id":"matrixBuilder","description":"Term-document matrix builder","type":"org.carrot2.text.vsm.TermDocumentMatrixBuilder","value":"TermDocumentMatrixBuilder","pathJava":"algorithmInstance.matrixBuilder","pathRest":"matrixBuilder","javadoc":{"text":"Configuration of the size and contents of the term-document matrix.","summary":"Configuration of the size and contents of the term-document matrix."},"implementations":{"TermDocumentMatrixBuilder":{"name":"TermDocumentMatrixBuilder","type":"org.carrot2.text.vsm.TermDocumentMatrixBuilder","javadoc":{"text":"Builds a term document matrix based on the provided <code>org.carrot2.text.preprocessing.PreprocessingContext</code>.","summary":"Builds a term document matrix based on the provided <code>org.carrot2.text.preprocessing.PreprocessingContext</code>."},"attributes":{"boostFields":{"id":"matrixBuilder.boostFields","description":"Boosted fields","type":"String[]","value":[],"pathJava":"algorithmInstance.matrixBuilder.boostFields","pathRest":"matrixBuilder.boostFields","javadoc":{"text":"A list fields for which to apply extra weight. Content of fields provided in this parameter can\\n be given more weight during clustering. You may want to boost, for example, the title field\\n with the assumption that it accurately summarizes the content of the whole document.","summary":"A list fields for which to apply extra weight."}},"boostedFieldWeight":{"id":"matrixBuilder.boostedFieldWeight","description":"Boosted fields weight","type":"Double","value":2,"constraints":["value >= 0.0","value <= 10.0"],"pathJava":"algorithmInstance.matrixBuilder.boostedFieldWeight","pathRest":"matrixBuilder.boostedFieldWeight","javadoc":{"text":"The extra weight to apply to words that appeared in boosted fields. The larger the value, the\\n stronger the boost.","summary":"The extra weight to apply to words that appeared in boosted fields."}},"maxWordDf":{"id":"matrixBuilder.maxWordDf","description":"Maximum word document frequency","type":"Double","value":0.9,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.matrixBuilder.maxWordDf","pathRest":"matrixBuilder.maxWordDf","javadoc":{"text":"Maximum document frequency allowed for words as a fraction of all documents. Words with\\n document frequency larger than <code>org.carrot2.text.vsm.TermDocumentMatrixBuilder#maxWordDf</code> will be ignored. For example, when <code>org.carrot2.text.vsm.TermDocumentMatrixBuilder#maxWordDf</code> is 0.4, words appearing in more than 40% of documents will be be ignored. A value\\n of 1.0 means that all words will be taken into account, no matter in how many documents they\\n appear.\\n\\n <p>This parameter may be useful when certain words appear in most of the input documents (e.g.\\n company name from header or footer) and such words dominate the cluster labels. In such case,\\n setting it to a value lower than 1.0 (e.g. 0.9) may improve the clusters.\\n\\n <p>Another useful application of this parameter is when there is a need to generate only very\\n specific clusters, that is clusters containing small numbers of documents. This can be achieved\\n by setting <code>org.carrot2.text.vsm.TermDocumentMatrixBuilder#maxWordDf</code> to extremely low values: 0.1 or 0.05.","summary":"Maximum document frequency allowed for words as a fraction of all documents."}},"maximumMatrixSize":{"id":"matrixBuilder.maximumMatrixSize","description":"Maximum term-document matrix size","type":"Integer","value":37500,"constraints":["value >= 5000"],"pathJava":"algorithmInstance.matrixBuilder.maximumMatrixSize","pathRest":"matrixBuilder.maximumMatrixSize","javadoc":{"text":"Maximum number of elements the term-document matrix can have. The larger the allowed matrix\\n size, the more accurate, time- and memory-consuming clustering.","summary":"Maximum number of elements the term-document matrix can have."}},"termWeighting":{"id":"matrixBuilder.termWeighting","description":"Term weighting for term-document matrix","type":"org.carrot2.text.vsm.TermWeighting","value":"LogTfIdfTermWeighting","pathJava":"algorithmInstance.matrixBuilder.termWeighting","pathRest":"matrixBuilder.termWeighting","javadoc":{"text":"Method for calculating weights of words in the term-document matrices.","summary":"Method for calculating weights of words in the term-document matrices."},"implementations":{"LinearTfIdfTermWeighting":{"name":"LinearTfIdfTermWeighting","type":"org.carrot2.text.vsm.LinearTfIdfTermWeighting","javadoc":{"text":"Calculates term-document matrix element values based on Linear Inverse Term Frequency.","summary":"Calculates term-document matrix element values based on Linear Inverse Term Frequency."},"attributes":{}},"LogTfIdfTermWeighting":{"name":"LogTfIdfTermWeighting","type":"org.carrot2.text.vsm.LogTfIdfTermWeighting","javadoc":{"text":"Calculates term-document matrix element values based on Log Inverse Term Frequency.","summary":"Calculates term-document matrix element values based on Log Inverse Term Frequency."},"attributes":{}},"TfTermWeighting":{"name":"TfTermWeighting","type":"org.carrot2.text.vsm.TfTermWeighting","javadoc":{"text":"Calculates term-document matrix element values based on Term Frequency.","summary":"Calculates term-document matrix element values based on Term Frequency."},"attributes":{}}}}}}}},"matrixReducer":{"id":"matrixReducer","description":"Term-document matrix reducer","type":"org.carrot2.text.vsm.TermDocumentMatrixReducer","value":"TermDocumentMatrixReducer","pathJava":"algorithmInstance.matrixReducer","pathRest":"matrixReducer","javadoc":{"text":"Configuration of the matrix decomposition method to use for clustering.","summary":"Configuration of the matrix decomposition method to use for clustering."},"implementations":{"TermDocumentMatrixReducer":{"name":"TermDocumentMatrixReducer","type":"org.carrot2.text.vsm.TermDocumentMatrixReducer","javadoc":{"text":"Reduces the dimensionality of a term-document matrix using a matrix factorization algorithm.","summary":"Reduces the dimensionality of a term-document matrix using a matrix factorization algorithm."},"attributes":{"factorizationFactory":{"id":"matrixReducer.factorizationFactory","description":"Term-document matrix factorization method","type":"org.carrot2.math.matrix.MatrixFactorizationFactory","value":"NonnegativeMatrixFactorizationEDFactory","pathJava":"algorithmInstance.matrixReducer.factorizationFactory","pathRest":"matrixReducer.factorizationFactory","javadoc":{"text":"Factorization method. The method to be used to factorize the term-document matrix and create\\n base vectors that will give rise to cluster labels.","summary":"Factorization method."},"implementations":{"KMeansMatrixFactorizationFactory":{"name":"KMeansMatrixFactorizationFactory","type":"org.carrot2.math.matrix.KMeansMatrixFactorizationFactory","javadoc":{"text":"Performs matrix factorization using the k-means clustering algorithm. This kind of factorization\\n is sometimes referred to as Concept Decomposition Factorization.","summary":"Performs matrix factorization using the k-means clustering algorithm."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::KMeansMatrixFactorizationFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.KMeansMatrixFactorizationFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"LocalNonnegativeMatrixFactorizationFactory":{"name":"LocalNonnegativeMatrixFactorizationFactory","type":"org.carrot2.math.matrix.LocalNonnegativeMatrixFactorizationFactory","javadoc":{"text":"Performs matrix factorization using the Local Non-negative Matrix Factorization algorithm with\\n minimization of the Kullback-Leibler divergence between A and UV\' and multiplicative updating.","summary":"Performs matrix factorization using the Local Non-negative Matrix Factorization algorithm with\\n minimization of the Kullback-Leibler divergence between A and UV\' and multiplicative updating."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::LocalNonnegativeMatrixFactorizationFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.LocalNonnegativeMatrixFactorizationFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"NonnegativeMatrixFactorizationEDFactory":{"name":"NonnegativeMatrixFactorizationEDFactory","type":"org.carrot2.math.matrix.NonnegativeMatrixFactorizationEDFactory","javadoc":{"text":"Performs matrix factorization using the Non-negative Matrix Factorization algorithm with\\n minimization of Euclidean Distance between A and UV\' and multiplicative updating.","summary":"Performs matrix factorization using the Non-negative Matrix Factorization algorithm with\\n minimization of Euclidean Distance between A and UV\' and multiplicative updating."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::NonnegativeMatrixFactorizationEDFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.NonnegativeMatrixFactorizationEDFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"NonnegativeMatrixFactorizationKLFactory":{"name":"NonnegativeMatrixFactorizationKLFactory","type":"org.carrot2.math.matrix.NonnegativeMatrixFactorizationKLFactory","javadoc":{"text":"Performs matrix factorization using the Non-negative Matrix Factorization by minimization of\\n Kullback-Leibler divergence between A and UV\' and multiplicative updating.","summary":"Performs matrix factorization using the Non-negative Matrix Factorization by minimization of\\n Kullback-Leibler divergence between A and UV\' and multiplicative updating."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::NonnegativeMatrixFactorizationKLFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.NonnegativeMatrixFactorizationKLFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"PartialSingularValueDecompositionFactory":{"name":"PartialSingularValueDecompositionFactory","type":"org.carrot2.math.matrix.PartialSingularValueDecompositionFactory","javadoc":{"text":"Performs matrix factorization using the Singular Value Decomposition algorithm.","summary":"Performs matrix factorization using the Singular Value Decomposition algorithm."},"attributes":{}}}}}}}},"preprocessing":{"id":"preprocessing","description":"Input preprocessing components","type":"org.carrot2.text.preprocessing.CompletePreprocessingPipeline","value":"CompletePreprocessingPipeline","pathJava":"algorithmInstance.preprocessing","pathRest":"preprocessing","javadoc":{"text":"Configuration of the text preprocessing stage.","summary":"Configuration of the text preprocessing stage."},"implementations":{"CompletePreprocessingPipeline":{"name":"CompletePreprocessingPipeline","type":"org.carrot2.text.preprocessing.CompletePreprocessingPipeline","javadoc":{"text":"Performs a complete preprocessing on the provided documents. The preprocessing consists of the\\n following steps:\\n\\n <ol>\\n   <li><code>org.carrot2.text.preprocessing.InputTokenizer</code>\\n   <li><code>org.carrot2.text.preprocessing.CaseNormalizer</code>\\n   <li><code>org.carrot2.text.preprocessing.LanguageModelStemmer</code>\\n   <li><code>org.carrot2.text.preprocessing.StopListMarker</code>\\n   <li><code>org.carrot2.text.preprocessing.PhraseExtractor</code>\\n   <li><code>org.carrot2.text.preprocessing.LabelFilterProcessor</code>\\n   <li><code>org.carrot2.text.preprocessing.DocumentAssigner</code>\\n </ol>","summary":"Performs a complete preprocessing on the provided documents."},"attributes":{"documentAssigner":{"id":"preprocessing.documentAssigner","description":"Control over cluster-document assignment","type":"org.carrot2.text.preprocessing.DocumentAssigner","value":"DocumentAssigner","pathJava":"algorithmInstance.preprocessing.documentAssigner","pathRest":"preprocessing.documentAssigner","javadoc":{"text":"Document assigner used by the algorithm, contains modifiable parameters..","summary":"Document assigner used by the algorithm, contains modifiable parameters.."},"implementations":{"DocumentAssigner":{"name":"DocumentAssigner","type":"org.carrot2.text.preprocessing.DocumentAssigner","javadoc":{"text":"Assigns document to label candidates. For each label candidate from <code>org.carrot2.text.preprocessing.PreprocessingContext.AllLabels#featureIndex</code> an <code>com.carrotsearch.hppc.BitSet</code> with the assigned documents is constructed. The\\n assignment algorithm is rather simple: in order to be assigned to a label, a document must\\n contain at least one occurrence of each non-stop word from the label.\\n\\n <p>This class saves the following results to the <code>org.carrot2.text.preprocessing.PreprocessingContext</code> :\\n\\n <ul>\\n   <li><code>org.carrot2.text.preprocessing.PreprocessingContext.AllLabels#documentIndices</code>\\n </ul>\\n\\n <p>This class requires that <code>org.carrot2.text.preprocessing.InputTokenizer</code>, <code>org.carrot2.text.preprocessing.CaseNormalizer</code>, <code>org.carrot2.text.preprocessing.StopListMarker</code>, <code>org.carrot2.text.preprocessing.PhraseExtractor</code> and <code>org.carrot2.text.preprocessing.LabelFilterProcessor</code> be invoked first.","summary":"Assigns document to label candidates."},"attributes":{"exactPhraseAssignment":{"id":"preprocessing.documentAssigner.exactPhraseAssignment","description":"Exact phrase assignment","type":"Boolean","value":false,"pathJava":"algorithmInstance.preprocessing.documentAssigner.exactPhraseAssignment","pathRest":"preprocessing.documentAssigner.exactPhraseAssignment","javadoc":{"text":"Only exact phrase assignments. When set to <code>true</code>, clusters will contain only the\\n documents that contain the cluster\'s label in its original form, including the order of words.\\n Enabling this option will cause fewer documents to be put in clusters, increasing the precision\\n of assignment, but also increasing the \\"Other Topics\\" group. Disabling this option will cause\\n more documents to be put in clusters, which will make the \\"Other Topics\\" cluster smaller, but\\n also lower the precision of cluster-document assignments.","summary":"Only exact phrase assignments."}},"minClusterSize":{"id":"preprocessing.documentAssigner.minClusterSize","description":"Minimum cluster size","type":"Integer","value":2,"constraints":["value >= 1","value <= 100"],"pathJava":"algorithmInstance.preprocessing.documentAssigner.minClusterSize","pathRest":"preprocessing.documentAssigner.minClusterSize","javadoc":{"text":"Minimum required number of documents in each cluster. Clusters containing fewer documents will\\n not be created.","summary":"Minimum required number of documents in each cluster."}}}}}},"labelFilters":{"id":"preprocessing.labelFilters","description":"Cluster label filters","type":"org.carrot2.text.preprocessing.LabelFilterProcessor","value":"LabelFilterProcessor","pathJava":"algorithmInstance.preprocessing.labelFilters","pathRest":"preprocessing.labelFilters","javadoc":{"text":"Label filtering is a composite of individual filters.","summary":"Label filtering is a composite of individual filters."},"implementations":{"LabelFilterProcessor":{"name":"LabelFilterProcessor","type":"org.carrot2.text.preprocessing.LabelFilterProcessor","javadoc":{"text":"Applies basic filtering to words and phrases to produce candidates for cluster labels. Filtering\\n is applied to <code>org.carrot2.text.preprocessing.PreprocessingContext.AllWords</code> and <code>org.carrot2.text.preprocessing.PreprocessingContext.AllPhrases</code>, the results are saved to <code>org.carrot2.text.preprocessing.PreprocessingContext.AllLabels</code>. Currently, the following filters are applied:\\n\\n <ol>\\n   <li><code>org.carrot2.text.preprocessing.filter.StopWordLabelFilter</code>\\n   <li><code>org.carrot2.text.preprocessing.filter.CompleteLabelFilter</code>\\n </ol>\\n\\n This class saves the following results to the <code>org.carrot2.text.preprocessing.PreprocessingContext</code>:\\n\\n <ul>\\n   <li><code>org.carrot2.text.preprocessing.PreprocessingContext.AllLabels#featureIndex</code>\\n </ul>\\n\\n <p>This class requires that <code>org.carrot2.text.preprocessing.InputTokenizer</code>, <code>org.carrot2.text.preprocessing.CaseNormalizer</code>, <code>org.carrot2.text.preprocessing.StopListMarker</code> and <code>org.carrot2.text.preprocessing.PhraseExtractor</code> be invoked first.","summary":"Applies basic filtering to words and phrases to produce candidates for cluster labels."},"attributes":{"completeLabelFilter":{"id":"preprocessing.labelFilters.completeLabelFilter","description":"Filters out labels that appear to be sub-sequences of other good candidate phrases","type":"org.carrot2.text.preprocessing.filter.CompleteLabelFilter","value":"CompleteLabelFilter","pathJava":"algorithmInstance.preprocessing.labelFilters.completeLabelFilter","pathRest":"preprocessing.labelFilters.completeLabelFilter","javadoc":{"text":"Truncated phrase filter for this processor.","summary":"Truncated phrase filter for this processor."},"implementations":{"CompleteLabelFilter":{"name":"CompleteLabelFilter","type":"org.carrot2.text.preprocessing.filter.CompleteLabelFilter","javadoc":{"text":"A filter that removes \\"incomplete\\" labels.\\n\\n <p>For example, in a collection of documents related to <i>Data Mining</i>, the phrase\\n <i>Conference on Data</i> is incomplete in a sense that most likely it should be <i>Conference on\\n Data Mining</i> or even <i>Conference on Data Mining in Large Databases</i>. When truncated\\n phrase removal is enabled, the algorithm would try to remove the \\"incomplete\\" phrases like the\\n former one and leave only the more informative variants.\\n\\n <p>See <a href=\\"http://project.carrot2.org/publications/osinski-2003-lingo.pdf\\">this\\n document</a>, page 31 for a definition of a complete phrase.","summary":"A filter that removes \\"incomplete\\" labels."},"attributes":{"enabled":{"id":"preprocessing.labelFilters.completeLabelFilter.enabled","description":"Truncated label filter enabled","type":"Boolean","value":true,"pathJava":"algorithmInstance.preprocessing.labelFilters.completeLabelFilter.enabled","pathRest":"preprocessing.labelFilters.completeLabelFilter.enabled","javadoc":{"text":"Enables or disables this filter.","summary":"Enables or disables this filter."}},"labelOverrideThreshold":{"id":"preprocessing.labelFilters.completeLabelFilter.labelOverrideThreshold","description":"Truncated label threshold","type":"Double","value":0.65,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.preprocessing.labelFilters.completeLabelFilter.labelOverrideThreshold","pathRest":"preprocessing.labelFilters.completeLabelFilter.labelOverrideThreshold","javadoc":{"text":"Determines the strength of the truncated label filter. The lowest value means strongest\\n truncated labels elimination, which may lead to overlong cluster labels and many unclustered\\n documents. The highest value effectively disables the filter, which may result in short or\\n truncated labels.","summary":"Determines the strength of the truncated label filter."}}}}}},"genitiveLabelFilter":{"id":"preprocessing.labelFilters.genitiveLabelFilter","description":"Filters out labels ending with Saxon Genitive (\'s)","type":"org.carrot2.text.preprocessing.filter.GenitiveLabelFilter","value":"GenitiveLabelFilter","pathJava":"algorithmInstance.preprocessing.labelFilters.genitiveLabelFilter","pathRest":"preprocessing.labelFilters.genitiveLabelFilter","javadoc":{"text":"Genitive length label filter.","summary":"Genitive length label filter."},"implementations":{"GenitiveLabelFilter":{"name":"GenitiveLabelFilter","type":"org.carrot2.text.preprocessing.filter.GenitiveLabelFilter","javadoc":{"text":"Removes labels that end in words in the Saxon Genitive form, for example <em>Threatening the\\n Country\'s</em>.","summary":"Removes labels that end in words in the Saxon Genitive form, for example <em>Threatening the\\n Country\'s</em>."},"attributes":{"enabled":{"id":"preprocessing.labelFilters.genitiveLabelFilter.enabled","description":"Genitive label filter enabled","type":"Boolean","value":true,"pathJava":"algorithmInstance.preprocessing.labelFilters.genitiveLabelFilter.enabled","pathRest":"preprocessing.labelFilters.genitiveLabelFilter.enabled","javadoc":{"text":"Enables or disables this filter.","summary":"Enables or disables this filter."}}}}}},"minLengthLabelFilter":{"id":"preprocessing.labelFilters.minLengthLabelFilter","description":"Filters out labels that are shorter than the provided threshold","type":"org.carrot2.text.preprocessing.filter.MinLengthLabelFilter","value":"MinLengthLabelFilter","pathJava":"algorithmInstance.preprocessing.labelFilters.minLengthLabelFilter","pathRest":"preprocessing.labelFilters.minLengthLabelFilter","javadoc":{"text":"Min length label filter.","summary":"Min length label filter."},"implementations":{"MinLengthLabelFilter":{"name":"MinLengthLabelFilter","type":"org.carrot2.text.preprocessing.filter.MinLengthLabelFilter","javadoc":{"text":"Removes labels whose length in characters is smaller than the provided value.","summary":"Removes labels whose length in characters is smaller than the provided value."},"attributes":{"enabled":{"id":"preprocessing.labelFilters.minLengthLabelFilter.enabled","description":"Minimum label length filter enabled","type":"Boolean","value":true,"pathJava":"algorithmInstance.preprocessing.labelFilters.minLengthLabelFilter.enabled","pathRest":"preprocessing.labelFilters.minLengthLabelFilter.enabled","javadoc":{"text":"Enables or disables this filter.","summary":"Enables or disables this filter."}},"minLength":{"id":"preprocessing.labelFilters.minLengthLabelFilter.minLength","description":"Minimum label length","type":"Integer","value":3,"pathJava":"algorithmInstance.preprocessing.labelFilters.minLengthLabelFilter.minLength","pathRest":"preprocessing.labelFilters.minLengthLabelFilter.minLength","javadoc":{"text":"Minimum required label length, in characters, inclusive.","summary":"Minimum required label length, in characters, inclusive."}}}}}},"numericLabelFilter":{"id":"preprocessing.labelFilters.numericLabelFilter","description":"Filters out labels that start with numerics","type":"org.carrot2.text.preprocessing.filter.NumericLabelFilter","value":"NumericLabelFilter","pathJava":"algorithmInstance.preprocessing.labelFilters.numericLabelFilter","pathRest":"preprocessing.labelFilters.numericLabelFilter","javadoc":{"text":"Numeric label filter for this processor.","summary":"Numeric label filter for this processor."},"implementations":{"NumericLabelFilter":{"name":"NumericLabelFilter","type":"org.carrot2.text.preprocessing.filter.NumericLabelFilter","javadoc":{"text":"Removes labels that start with a numeric token.","summary":"Removes labels that start with a numeric token."},"attributes":{"enabled":{"id":"preprocessing.labelFilters.numericLabelFilter.enabled","description":"Numeric label filter enabled","type":"Boolean","value":true,"pathJava":"algorithmInstance.preprocessing.labelFilters.numericLabelFilter.enabled","pathRest":"preprocessing.labelFilters.numericLabelFilter.enabled","javadoc":{"text":"Enables or disables this filter.","summary":"Enables or disables this filter."}}}}}},"queryLabelFilter":{"id":"preprocessing.labelFilters.queryLabelFilter","description":"Filters out labels consisting of query hint terms","type":"org.carrot2.text.preprocessing.filter.QueryLabelFilter","value":"QueryLabelFilter","pathJava":"algorithmInstance.preprocessing.labelFilters.queryLabelFilter","pathRest":"preprocessing.labelFilters.queryLabelFilter","javadoc":{"text":"Query word label filter for this processor.","summary":"Query word label filter for this processor."},"implementations":{"QueryLabelFilter":{"name":"QueryLabelFilter","type":"org.carrot2.text.preprocessing.filter.QueryLabelFilter","javadoc":{"text":"Removes labels that consist only of query words.","summary":"Removes labels that consist only of query words."},"attributes":{"enabled":{"id":"preprocessing.labelFilters.queryLabelFilter.enabled","description":"Query label filter enabled","type":"Boolean","value":true,"pathJava":"algorithmInstance.preprocessing.labelFilters.queryLabelFilter.enabled","pathRest":"preprocessing.labelFilters.queryLabelFilter.enabled","javadoc":{"text":"Enables or disables this filter.","summary":"Enables or disables this filter."}}}}}},"stopLabelFilter":{"id":"preprocessing.labelFilters.stopLabelFilter","description":"Filters out labels tagged ignorable by the lexical data filters","type":"org.carrot2.text.preprocessing.filter.StopLabelFilter","value":"StopLabelFilter","pathJava":"algorithmInstance.preprocessing.labelFilters.stopLabelFilter","pathRest":"preprocessing.labelFilters.stopLabelFilter","javadoc":{"text":"Stop label filter.","summary":"Stop label filter."},"implementations":{"StopLabelFilter":{"name":"StopLabelFilter","type":"org.carrot2.text.preprocessing.filter.StopLabelFilter","javadoc":{"text":"Removes labels that are declared as stop labels in the <code>stoplabels.&lt;lang&gt;</code> files (or are\\n filtered out by <code>org.carrot2.language.EphemeralDictionaries</code>.","summary":"Removes labels that are declared as stop labels in the <code>stoplabels.&lt;lang&gt;</code> files (or are\\n filtered out by <code>org.carrot2.language.EphemeralDictionaries</code>."},"attributes":{"enabled":{"id":"preprocessing.labelFilters.stopLabelFilter.enabled","description":"Stop label filter enabled","type":"Boolean","value":true,"pathJava":"algorithmInstance.preprocessing.labelFilters.stopLabelFilter.enabled","pathRest":"preprocessing.labelFilters.stopLabelFilter.enabled","javadoc":{"text":"Enables or disables this filter.","summary":"Enables or disables this filter."}}}}}},"stopWordLabelFilter":{"id":"preprocessing.labelFilters.stopWordLabelFilter","description":"Filters out labels starting or ending with ignorable words","type":"org.carrot2.text.preprocessing.filter.StopWordLabelFilter","value":"StopWordLabelFilter","pathJava":"algorithmInstance.preprocessing.labelFilters.stopWordLabelFilter","pathRest":"preprocessing.labelFilters.stopWordLabelFilter","javadoc":{"text":"Stop word label filter for this processor.","summary":"Stop word label filter for this processor."},"implementations":{"StopWordLabelFilter":{"name":"StopWordLabelFilter","type":"org.carrot2.text.preprocessing.filter.StopWordLabelFilter","javadoc":{"text":"Removes labels that start or end in a stop word.","summary":"Removes labels that start or end in a stop word."},"attributes":{"enabled":{"id":"preprocessing.labelFilters.stopWordLabelFilter.enabled","description":"Stop word label filter enabled","type":"Boolean","value":true,"pathJava":"algorithmInstance.preprocessing.labelFilters.stopWordLabelFilter.enabled","pathRest":"preprocessing.labelFilters.stopWordLabelFilter.enabled","javadoc":{"text":"Enables or disables this filter.","summary":"Enables or disables this filter."}}}}}}}}}},"phraseDfThreshold":{"id":"preprocessing.phraseDfThreshold","description":"Phrase document frequency threshold","type":"Integer","value":1,"constraints":["value >= 1","value <= 100"],"pathJava":"algorithmInstance.preprocessing.phraseDfThreshold","pathRest":"preprocessing.phraseDfThreshold","javadoc":{"text":"Phrase Document Frequency cut-off threshold. Phrases appearing in fewer than <code>\\n phraseDfThreshold</code> documents will be ignored.","summary":"Phrase Document Frequency cut-off threshold."}},"wordDfThreshold":{"id":"preprocessing.wordDfThreshold","description":"Word document frequency threshold","type":"Integer","value":1,"constraints":["value >= 1","value <= 100"],"pathJava":"algorithmInstance.preprocessing.wordDfThreshold","pathRest":"preprocessing.wordDfThreshold","javadoc":{"text":"Word Document Frequency cut-off threshold. Words appearing in fewer than <code>wordDfThreshold\\n </code> documents will be ignored.","summary":"Word Document Frequency cut-off threshold."}}}}}},"queryHint":{"id":"queryHint","description":"Query hint","type":"String","value":null,"pathJava":"algorithmInstance.queryHint","pathRest":"queryHint","javadoc":{"text":"Query terms used to retrieve documents being clustered. The query is used as a hint to avoid\\n creating trivial clusters consisting only of query words.","summary":"Query terms used to retrieve documents being clustered."}},"scoreWeight":{"id":"scoreWeight","description":"Size-score sorting ratio","type":"Double","value":0,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.scoreWeight","pathRest":"scoreWeight","javadoc":{"text":"Balance between cluster score and size during cluster sorting. Value equal to 0.0 will cause\\n Lingo to sort clusters based only on cluster size. Value equal to 1.0 will cause Lingo to sort\\n clusters based only on cluster score.","summary":"Balance between cluster score and size during cluster sorting."}}}}')
}, , , function (e) {
    e.exports = JSON.parse('{"name":"STC","type":"org.carrot2.clustering.stc.STCClusteringAlgorithm","javadoc":{"text":"Suffix Tree Clustering (STC) algorithm. Pretty much as described in: <i>Oren Zamir, Oren Etzioni,\\n Grouper: A Dynamic Clustering Interface to Web Search Results, 1999.</i> Some liberties were\\n taken wherever STC\'s description was not clear enough or where we thought some improvements could\\n be made.","summary":"Suffix Tree Clustering (STC) algorithm."},"attributes":{"dictionaries":{"id":"dictionaries","description":"Per-request overrides of language components","type":"org.carrot2.language.EphemeralDictionaries","value":"EphemeralDictionaries","pathJava":"algorithmInstance.dictionaries","pathRest":"dictionaries","javadoc":{"text":"Per-request overrides of language components (dictionaries).","summary":"Per-request overrides of language components (dictionaries)."},"implementations":{"EphemeralDictionaries":{"name":"EphemeralDictionaries","type":"org.carrot2.language.EphemeralDictionaries","javadoc":{"text":"Ephemeral per-request overrides for the default <code>org.carrot2.language.LanguageComponents</code> passed to the\\n algorithm.","summary":"Ephemeral per-request overrides for the default <code>org.carrot2.language.LanguageComponents</code> passed to the\\n algorithm."},"attributes":{"labelFilters":{"id":"dictionaries.labelFilters","description":"Cluster label filtering dictionaries.","type":"org.carrot2.language.LabelFilterDictionary[]","value":[],"pathJava":"algorithmInstance.dictionaries.labelFilters","pathRest":"dictionaries.labelFilters","javadoc":{"text":"Additional label filtering dictionaries (supplying cluster label filters that should be\\n discarded from the output).\\n\\n <p>One or more dictionaries can be supplied. The default implementation in <code>org.carrot2.language.DefaultDictionaryImpl</code> supports exact string matching and regular expression patterns.\\n\\n <p>REST-style example using the default implementation:\\n\\n <pre><code>&quot;labelFilters&quot;: [{\\n   &quot;exact&quot;: [&quot;Cluster Label 1&quot;, &quot;Foo Bar&quot;],\\n   &quot;regexp&quot;: [\\n     &quot;(?).+pattern1.+&quot;,\\n     &quot;(?).+[0-9]{2}.+&quot;\\n   ]\\n }]</code></pre>","summary":"Additional label filtering dictionaries (supplying cluster label filters that should be\\n discarded from the output)."}},"wordFilters":{"id":"dictionaries.wordFilters","description":"Word filtering dictionaries.","type":"org.carrot2.language.StopwordFilterDictionary[]","value":[],"pathJava":"algorithmInstance.dictionaries.wordFilters","pathRest":"dictionaries.wordFilters","javadoc":{"text":"Additional stop word filtering dictionaries (supplying word filters that should be discarded\\n from the input).\\n\\n <p>One or more dictionaries can be supplied. The default implementation in <code>org.carrot2.language.DefaultDictionaryImpl</code> supports exact string matching and regular expression patterns.\\n\\n <p>REST-style example using the default implementation:\\n\\n <pre><code>&quot;wordFilters&quot;: [{\\n   &quot;exact&quot;: [&quot;word1&quot;, &quot;word2&quot;],\\n   &quot;regexp&quot;: [\\n     &quot;(?).+pattern1.+&quot;,\\n     &quot;(?).+[0-9]{2}.+&quot;\\n   ]\\n }]</code></pre>","summary":"Additional stop word filtering dictionaries (supplying word filters that should be discarded\\n from the input)."}}}}}},"documentCountBoost":{"id":"documentCountBoost","description":"Document count boost","type":"Double","value":1,"constraints":["value >= 0.0"],"pathJava":"algorithmInstance.documentCountBoost","pathRest":"documentCountBoost","javadoc":{"text":"Base cluster document count boost. A factor in calculation of the base cluster score, boosting\\n the score depending on the number of documents found in the base cluster.","summary":"Base cluster document count boost."}},"ignoreWordIfInHigherDocsPercent":{"id":"ignoreWordIfInHigherDocsPercent","description":"Maximum word-document ratio","type":"Double","value":0.9,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.ignoreWordIfInHigherDocsPercent","pathRest":"ignoreWordIfInHigherDocsPercent","javadoc":{"text":"Ignore words appearing in more than the provided fraction of documents. A number between 0 and\\n 1, if a word exists in more snippets than this ratio, it is ignored.","summary":"Ignore words appearing in more than the provided fraction of documents."}},"maxBaseClusters":{"id":"maxBaseClusters","description":"Maximum base clusters","type":"Integer","value":300,"constraints":["value >= 2"],"pathJava":"algorithmInstance.maxBaseClusters","pathRest":"maxBaseClusters","javadoc":{"text":"Maximum number of base cluster. Trims the base cluster array after N-th position for the\\n merging phase.","summary":"Maximum number of base cluster."}},"maxClusters":{"id":"maxClusters","description":"Maximum number of final clusters","type":"Integer","value":15,"constraints":["value >= 1"],"pathJava":"algorithmInstance.maxClusters","pathRest":"maxClusters","javadoc":{"text":"Maximum number final clusters to keep. Clusters beyond the maximum will be discarded.","summary":"Maximum number final clusters to keep."}},"maxPhraseOverlap":{"id":"maxPhraseOverlap","description":"Maximum cluster phrase overlap","type":"Double","value":0.6,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.maxPhraseOverlap","pathRest":"maxPhraseOverlap","javadoc":{"text":"Maximum cluster phrase overlap.","summary":"Maximum cluster phrase overlap."}},"maxPhrasesPerLabel":{"id":"maxPhrasesPerLabel","description":"Maximum phrases per label","type":"Integer","value":3,"constraints":["value >= 1"],"pathJava":"algorithmInstance.maxPhrasesPerLabel","pathRest":"maxPhrasesPerLabel","javadoc":{"text":"Maximum number of phrases from base clusters to promote to the cluster\'s label.","summary":"Maximum number of phrases from base clusters to promote to the cluster\'s label."}},"maxWordsPerLabel":{"id":"maxWordsPerLabel","description":"Maximum words per label","type":"Integer","value":4,"constraints":["value >= 1"],"pathJava":"algorithmInstance.maxWordsPerLabel","pathRest":"maxWordsPerLabel","javadoc":{"text":"Maximum allowed number of words per label. Base clusters formed by phrases with more words than\\n this ratio will be trimmed.","summary":"Maximum allowed number of words per label."}},"mergeStemEquivalentBaseClusters":{"id":"mergeStemEquivalentBaseClusters","description":"Merge all stem-equivalent phrases when discovering base clusters","type":"Boolean","value":true,"pathJava":"algorithmInstance.mergeStemEquivalentBaseClusters","pathRest":"mergeStemEquivalentBaseClusters","javadoc":{"text":"Merge all stem-equivalent base clusters before running the merge phase.","summary":"Merge all stem-equivalent base clusters before running the merge phase."}},"mergeThreshold":{"id":"mergeThreshold","description":"Base cluster merge threshold","type":"Double","value":0.6,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.mergeThreshold","pathRest":"mergeThreshold","javadoc":{"text":"Base cluster merge threshold.","summary":"Base cluster merge threshold."}},"minBaseClusterScore":{"id":"minBaseClusterScore","description":"Minimum base cluster score","type":"Double","value":2,"constraints":["value >= 0.0","value <= 10.0"],"pathJava":"algorithmInstance.minBaseClusterScore","pathRest":"minBaseClusterScore","javadoc":{"text":"Minimum base cluster score, before coverage merging.","summary":"Minimum base cluster score, before coverage merging."}},"minBaseClusterSize":{"id":"minBaseClusterSize","description":"Minimum base cluster documents","type":"Integer","value":2,"constraints":["value >= 2","value <= 20"],"pathJava":"algorithmInstance.minBaseClusterSize","pathRest":"minBaseClusterSize","javadoc":{"text":"Minimum required number of documents in a base cluster.","summary":"Minimum required number of documents in a base cluster."}},"mostGeneralPhraseCoverage":{"id":"mostGeneralPhraseCoverage","description":"Minimum general phrase coverage","type":"Double","value":0.5,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.mostGeneralPhraseCoverage","pathRest":"mostGeneralPhraseCoverage","javadoc":{"text":"Minimum coverage required for a phrase to appear in cluster description.","summary":"Minimum coverage required for a phrase to appear in cluster description."}},"optimalPhraseLength":{"id":"optimalPhraseLength","description":"Optimal cluster label length","type":"Integer","value":3,"constraints":["value >= 1"],"pathJava":"algorithmInstance.optimalPhraseLength","pathRest":"optimalPhraseLength","javadoc":{"text":"Optimal label length. A factor in calculation of the base cluster score.","summary":"Optimal label length."}},"optimalPhraseLengthDev":{"id":"optimalPhraseLengthDev","description":"Phrase length tolerance","type":"Double","value":2,"constraints":["value >= 0.5"],"pathJava":"algorithmInstance.optimalPhraseLengthDev","pathRest":"optimalPhraseLengthDev","javadoc":{"text":"Optimal cluster label length\'s tolerance. A factor in calculation of the base cluster score.","summary":"Optimal cluster label length\'s tolerance."}},"preprocessing":{"id":"preprocessing","description":"Input preprocessing components","type":"org.carrot2.text.preprocessing.BasicPreprocessingPipeline","value":"BasicPreprocessingPipeline","pathJava":"algorithmInstance.preprocessing","pathRest":"preprocessing","javadoc":{"text":"Configuration of the text preprocessing stage.","summary":"Configuration of the text preprocessing stage."},"implementations":{"BasicPreprocessingPipeline":{"name":"BasicPreprocessingPipeline","type":"org.carrot2.text.preprocessing.BasicPreprocessingPipeline","javadoc":{"text":"Performs basic preprocessing steps on the provided documents. The preprocessing consists of the\\n following steps:\\n\\n <ol>\\n   <li><code>org.carrot2.text.preprocessing.InputTokenizer</code>\\n   <li><code>org.carrot2.text.preprocessing.CaseNormalizer</code>\\n   <li><code>org.carrot2.text.preprocessing.LanguageModelStemmer</code>\\n   <li><code>org.carrot2.text.preprocessing.StopListMarker</code>\\n </ol>","summary":"Performs basic preprocessing steps on the provided documents."},"attributes":{"wordDfThreshold":{"id":"preprocessing.wordDfThreshold","description":"Word document frequency threshold","type":"Integer","value":1,"constraints":["value >= 1","value <= 100"],"pathJava":"algorithmInstance.preprocessing.wordDfThreshold","pathRest":"preprocessing.wordDfThreshold","javadoc":{"text":"Word Document Frequency threshold. Words appearing in fewer than <code>dfThreshold</code>\\n documents will be ignored.","summary":"Word Document Frequency threshold."}}}}}},"queryHint":{"id":"queryHint","description":"Query hint","type":"String","value":null,"pathJava":"algorithmInstance.queryHint","pathRest":"queryHint","javadoc":{"text":"Query terms used to retrieve documents. The query is used as a hint to avoid trivial clusters.","summary":"Query terms used to retrieve documents."}},"scoreWeight":{"id":"scoreWeight","description":"Size-score sorting ratio","type":"Double","value":0,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.scoreWeight","pathRest":"scoreWeight","javadoc":{"text":"Balance between cluster score and size during cluster sorting. Value equal to 0.0 will sort\\n clusters based only on cluster size. Value equal to 1.0 will sort clusters based only on\\n cluster score.","summary":"Balance between cluster score and size during cluster sorting."}},"singleTermBoost":{"id":"singleTermBoost","description":"Boost single-term clusters","type":"Double","value":0.5,"constraints":["value >= 0.0"],"pathJava":"algorithmInstance.singleTermBoost","pathRest":"singleTermBoost","javadoc":{"text":"Base cluster score override for single-term clusters. If greater then zero, single-term base\\n clusters are assigned this value regardless of the penalty function.","summary":"Base cluster score override for single-term clusters."}}}}')
}, function (e) {
    e.exports = JSON.parse('{"name":"Bisecting K-Means","type":"org.carrot2.clustering.kmeans.BisectingKMeansClusteringAlgorithm","javadoc":{"text":"A very simple implementation of bisecting k-means clustering. Unlike other algorithms in Carrot2,\\n this one creates hard clustering (one document belongs only to one cluster). On the other hand,\\n the clusters are labeled only with individual words that may not always fully correspond to all\\n documents in the cluster.","summary":"A very simple implementation of bisecting k-means clustering."},"attributes":{"clusterCount":{"id":"clusterCount","description":"Cluster count","type":"Integer","value":25,"constraints":["value >= 2"],"pathJava":"algorithmInstance.clusterCount","pathRest":"clusterCount","javadoc":{"text":"Number of clusters to create. The algorithm will create at most the specified number of\\n clusters.","summary":"Number of clusters to create."}},"dictionaries":{"id":"dictionaries","description":"Per-request overrides of language components","type":"org.carrot2.language.EphemeralDictionaries","value":"EphemeralDictionaries","pathJava":"algorithmInstance.dictionaries","pathRest":"dictionaries","javadoc":{"text":"Per-request overrides of language components (dictionaries).","summary":"Per-request overrides of language components (dictionaries)."},"implementations":{"EphemeralDictionaries":{"name":"EphemeralDictionaries","type":"org.carrot2.language.EphemeralDictionaries","javadoc":{"text":"Ephemeral per-request overrides for the default <code>org.carrot2.language.LanguageComponents</code> passed to the\\n algorithm.","summary":"Ephemeral per-request overrides for the default <code>org.carrot2.language.LanguageComponents</code> passed to the\\n algorithm."},"attributes":{"labelFilters":{"id":"dictionaries.labelFilters","description":"Cluster label filtering dictionaries.","type":"org.carrot2.language.LabelFilterDictionary[]","value":[],"pathJava":"algorithmInstance.dictionaries.labelFilters","pathRest":"dictionaries.labelFilters","javadoc":{"text":"Additional label filtering dictionaries (supplying cluster label filters that should be\\n discarded from the output).\\n\\n <p>One or more dictionaries can be supplied. The default implementation in <code>org.carrot2.language.DefaultDictionaryImpl</code> supports exact string matching and regular expression patterns.\\n\\n <p>REST-style example using the default implementation:\\n\\n <pre><code>&quot;labelFilters&quot;: [{\\n   &quot;exact&quot;: [&quot;Cluster Label 1&quot;, &quot;Foo Bar&quot;],\\n   &quot;regexp&quot;: [\\n     &quot;(?).+pattern1.+&quot;,\\n     &quot;(?).+[0-9]{2}.+&quot;\\n   ]\\n }]</code></pre>","summary":"Additional label filtering dictionaries (supplying cluster label filters that should be\\n discarded from the output)."}},"wordFilters":{"id":"dictionaries.wordFilters","description":"Word filtering dictionaries.","type":"org.carrot2.language.StopwordFilterDictionary[]","value":[],"pathJava":"algorithmInstance.dictionaries.wordFilters","pathRest":"dictionaries.wordFilters","javadoc":{"text":"Additional stop word filtering dictionaries (supplying word filters that should be discarded\\n from the input).\\n\\n <p>One or more dictionaries can be supplied. The default implementation in <code>org.carrot2.language.DefaultDictionaryImpl</code> supports exact string matching and regular expression patterns.\\n\\n <p>REST-style example using the default implementation:\\n\\n <pre><code>&quot;wordFilters&quot;: [{\\n   &quot;exact&quot;: [&quot;word1&quot;, &quot;word2&quot;],\\n   &quot;regexp&quot;: [\\n     &quot;(?).+pattern1.+&quot;,\\n     &quot;(?).+[0-9]{2}.+&quot;\\n   ]\\n }]</code></pre>","summary":"Additional stop word filtering dictionaries (supplying word filters that should be discarded\\n from the input)."}}}}}},"labelCount":{"id":"labelCount","description":"Label count","type":"Integer","value":3,"constraints":["value >= 1","value <= 10"],"pathJava":"algorithmInstance.labelCount","pathRest":"labelCount","javadoc":{"text":"Minimum number of labels to return for each cluster.","summary":"Minimum number of labels to return for each cluster."}},"matrixBuilder":{"id":"matrixBuilder","description":"Term-document matrix builder","type":"org.carrot2.text.vsm.TermDocumentMatrixBuilder","value":"TermDocumentMatrixBuilder","pathJava":"algorithmInstance.matrixBuilder","pathRest":"matrixBuilder","javadoc":{"text":"Configuration of the size and contents of the term-document matrix.","summary":"Configuration of the size and contents of the term-document matrix."},"implementations":{"TermDocumentMatrixBuilder":{"name":"TermDocumentMatrixBuilder","type":"org.carrot2.text.vsm.TermDocumentMatrixBuilder","javadoc":{"text":"Builds a term document matrix based on the provided <code>org.carrot2.text.preprocessing.PreprocessingContext</code>.","summary":"Builds a term document matrix based on the provided <code>org.carrot2.text.preprocessing.PreprocessingContext</code>."},"attributes":{"boostFields":{"id":"matrixBuilder.boostFields","description":"Boosted fields","type":"String[]","value":[],"pathJava":"algorithmInstance.matrixBuilder.boostFields","pathRest":"matrixBuilder.boostFields","javadoc":{"text":"A list fields for which to apply extra weight. Content of fields provided in this parameter can\\n be given more weight during clustering. You may want to boost, for example, the title field\\n with the assumption that it accurately summarizes the content of the whole document.","summary":"A list fields for which to apply extra weight."}},"boostedFieldWeight":{"id":"matrixBuilder.boostedFieldWeight","description":"Boosted fields weight","type":"Double","value":2,"constraints":["value >= 0.0","value <= 10.0"],"pathJava":"algorithmInstance.matrixBuilder.boostedFieldWeight","pathRest":"matrixBuilder.boostedFieldWeight","javadoc":{"text":"The extra weight to apply to words that appeared in boosted fields. The larger the value, the\\n stronger the boost.","summary":"The extra weight to apply to words that appeared in boosted fields."}},"maxWordDf":{"id":"matrixBuilder.maxWordDf","description":"Maximum word document frequency","type":"Double","value":0.9,"constraints":["value >= 0.0","value <= 1.0"],"pathJava":"algorithmInstance.matrixBuilder.maxWordDf","pathRest":"matrixBuilder.maxWordDf","javadoc":{"text":"Maximum document frequency allowed for words as a fraction of all documents. Words with\\n document frequency larger than <code>org.carrot2.text.vsm.TermDocumentMatrixBuilder#maxWordDf</code> will be ignored. For example, when <code>org.carrot2.text.vsm.TermDocumentMatrixBuilder#maxWordDf</code> is 0.4, words appearing in more than 40% of documents will be be ignored. A value\\n of 1.0 means that all words will be taken into account, no matter in how many documents they\\n appear.\\n\\n <p>This parameter may be useful when certain words appear in most of the input documents (e.g.\\n company name from header or footer) and such words dominate the cluster labels. In such case,\\n setting it to a value lower than 1.0 (e.g. 0.9) may improve the clusters.\\n\\n <p>Another useful application of this parameter is when there is a need to generate only very\\n specific clusters, that is clusters containing small numbers of documents. This can be achieved\\n by setting <code>org.carrot2.text.vsm.TermDocumentMatrixBuilder#maxWordDf</code> to extremely low values: 0.1 or 0.05.","summary":"Maximum document frequency allowed for words as a fraction of all documents."}},"maximumMatrixSize":{"id":"matrixBuilder.maximumMatrixSize","description":"Maximum term-document matrix size","type":"Integer","value":37500,"constraints":["value >= 5000"],"pathJava":"algorithmInstance.matrixBuilder.maximumMatrixSize","pathRest":"matrixBuilder.maximumMatrixSize","javadoc":{"text":"Maximum number of elements the term-document matrix can have. The larger the allowed matrix\\n size, the more accurate, time- and memory-consuming clustering.","summary":"Maximum number of elements the term-document matrix can have."}},"termWeighting":{"id":"matrixBuilder.termWeighting","description":"Term weighting for term-document matrix","type":"org.carrot2.text.vsm.TermWeighting","value":"LogTfIdfTermWeighting","pathJava":"algorithmInstance.matrixBuilder.termWeighting","pathRest":"matrixBuilder.termWeighting","javadoc":{"text":"Method for calculating weights of words in the term-document matrices.","summary":"Method for calculating weights of words in the term-document matrices."},"implementations":{"LinearTfIdfTermWeighting":{"name":"LinearTfIdfTermWeighting","type":"org.carrot2.text.vsm.LinearTfIdfTermWeighting","javadoc":{"text":"Calculates term-document matrix element values based on Linear Inverse Term Frequency.","summary":"Calculates term-document matrix element values based on Linear Inverse Term Frequency."},"attributes":{}},"LogTfIdfTermWeighting":{"name":"LogTfIdfTermWeighting","type":"org.carrot2.text.vsm.LogTfIdfTermWeighting","javadoc":{"text":"Calculates term-document matrix element values based on Log Inverse Term Frequency.","summary":"Calculates term-document matrix element values based on Log Inverse Term Frequency."},"attributes":{}},"TfTermWeighting":{"name":"TfTermWeighting","type":"org.carrot2.text.vsm.TfTermWeighting","javadoc":{"text":"Calculates term-document matrix element values based on Term Frequency.","summary":"Calculates term-document matrix element values based on Term Frequency."},"attributes":{}}}}}}}},"matrixReducer":{"id":"matrixReducer","description":"Term-document matrix reducer","type":"org.carrot2.text.vsm.TermDocumentMatrixReducer","value":"TermDocumentMatrixReducer","pathJava":"algorithmInstance.matrixReducer","pathRest":"matrixReducer","javadoc":{"text":"Configuration of the matrix decomposition method to use for clustering.","summary":"Configuration of the matrix decomposition method to use for clustering."},"implementations":{"TermDocumentMatrixReducer":{"name":"TermDocumentMatrixReducer","type":"org.carrot2.text.vsm.TermDocumentMatrixReducer","javadoc":{"text":"Reduces the dimensionality of a term-document matrix using a matrix factorization algorithm.","summary":"Reduces the dimensionality of a term-document matrix using a matrix factorization algorithm."},"attributes":{"factorizationFactory":{"id":"matrixReducer.factorizationFactory","description":"Term-document matrix factorization method","type":"org.carrot2.math.matrix.MatrixFactorizationFactory","value":"NonnegativeMatrixFactorizationEDFactory","pathJava":"algorithmInstance.matrixReducer.factorizationFactory","pathRest":"matrixReducer.factorizationFactory","javadoc":{"text":"Factorization method. The method to be used to factorize the term-document matrix and create\\n base vectors that will give rise to cluster labels.","summary":"Factorization method."},"implementations":{"KMeansMatrixFactorizationFactory":{"name":"KMeansMatrixFactorizationFactory","type":"org.carrot2.math.matrix.KMeansMatrixFactorizationFactory","javadoc":{"text":"Performs matrix factorization using the k-means clustering algorithm. This kind of factorization\\n is sometimes referred to as Concept Decomposition Factorization.","summary":"Performs matrix factorization using the k-means clustering algorithm."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::KMeansMatrixFactorizationFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.KMeansMatrixFactorizationFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"LocalNonnegativeMatrixFactorizationFactory":{"name":"LocalNonnegativeMatrixFactorizationFactory","type":"org.carrot2.math.matrix.LocalNonnegativeMatrixFactorizationFactory","javadoc":{"text":"Performs matrix factorization using the Local Non-negative Matrix Factorization algorithm with\\n minimization of the Kullback-Leibler divergence between A and UV\' and multiplicative updating.","summary":"Performs matrix factorization using the Local Non-negative Matrix Factorization algorithm with\\n minimization of the Kullback-Leibler divergence between A and UV\' and multiplicative updating."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::LocalNonnegativeMatrixFactorizationFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.LocalNonnegativeMatrixFactorizationFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"NonnegativeMatrixFactorizationEDFactory":{"name":"NonnegativeMatrixFactorizationEDFactory","type":"org.carrot2.math.matrix.NonnegativeMatrixFactorizationEDFactory","javadoc":{"text":"Performs matrix factorization using the Non-negative Matrix Factorization algorithm with\\n minimization of Euclidean Distance between A and UV\' and multiplicative updating.","summary":"Performs matrix factorization using the Non-negative Matrix Factorization algorithm with\\n minimization of Euclidean Distance between A and UV\' and multiplicative updating."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::NonnegativeMatrixFactorizationEDFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.NonnegativeMatrixFactorizationEDFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"NonnegativeMatrixFactorizationKLFactory":{"name":"NonnegativeMatrixFactorizationKLFactory","type":"org.carrot2.math.matrix.NonnegativeMatrixFactorizationKLFactory","javadoc":{"text":"Performs matrix factorization using the Non-negative Matrix Factorization by minimization of\\n Kullback-Leibler divergence between A and UV\' and multiplicative updating.","summary":"Performs matrix factorization using the Non-negative Matrix Factorization by minimization of\\n Kullback-Leibler divergence between A and UV\' and multiplicative updating."},"attributes":{"factorizationQuality":{"id":"matrixReducer.factorizationFactory::NonnegativeMatrixFactorizationKLFactory.factorizationQuality","description":"Factorization quality","type":"org.carrot2.math.matrix.FactorizationQuality","value":"HIGH","constraints":["value in [LOW, MEDIUM, HIGH]"],"pathJava":"((org.carrot2.math.matrix.NonnegativeMatrixFactorizationKLFactory) algorithmInstance.matrixReducer.factorizationFactory).factorizationQuality","pathRest":"matrixReducer.factorizationFactory.factorizationQuality","javadoc":{"text":"Number of iterations of matrix factorization to perform. The higher the required quality, the\\n more time-consuming clustering.","summary":"Number of iterations of matrix factorization to perform."}}}},"PartialSingularValueDecompositionFactory":{"name":"PartialSingularValueDecompositionFactory","type":"org.carrot2.math.matrix.PartialSingularValueDecompositionFactory","javadoc":{"text":"Performs matrix factorization using the Singular Value Decomposition algorithm.","summary":"Performs matrix factorization using the Singular Value Decomposition algorithm."},"attributes":{}}}}}}}},"maxIterations":{"id":"maxIterations","description":"Maximum iterations","type":"Integer","value":15,"constraints":["value >= 1"],"pathJava":"algorithmInstance.maxIterations","pathRest":"maxIterations","javadoc":{"text":"Maximum number of k-means iterations to perform.","summary":"Maximum number of k-means iterations to perform."}},"partitionCount":{"id":"partitionCount","description":"Partition count","type":"Integer","value":2,"constraints":["value >= 2","value <= 10"],"pathJava":"algorithmInstance.partitionCount","pathRest":"partitionCount","javadoc":{"text":"Number of partitions to create at each k-means clustering iteration.","summary":"Number of partitions to create at each k-means clustering iteration."}},"preprocessing":{"id":"preprocessing","description":"Input preprocessing components","type":"org.carrot2.text.preprocessing.BasicPreprocessingPipeline","value":"BasicPreprocessingPipeline","pathJava":"algorithmInstance.preprocessing","pathRest":"preprocessing","javadoc":{"text":"Configuration of the text preprocessing stage.","summary":"Configuration of the text preprocessing stage."},"implementations":{"BasicPreprocessingPipeline":{"name":"BasicPreprocessingPipeline","type":"org.carrot2.text.preprocessing.BasicPreprocessingPipeline","javadoc":{"text":"Performs basic preprocessing steps on the provided documents. The preprocessing consists of the\\n following steps:\\n\\n <ol>\\n   <li><code>org.carrot2.text.preprocessing.InputTokenizer</code>\\n   <li><code>org.carrot2.text.preprocessing.CaseNormalizer</code>\\n   <li><code>org.carrot2.text.preprocessing.LanguageModelStemmer</code>\\n   <li><code>org.carrot2.text.preprocessing.StopListMarker</code>\\n </ol>","summary":"Performs basic preprocessing steps on the provided documents."},"attributes":{"wordDfThreshold":{"id":"preprocessing.wordDfThreshold","description":"Word document frequency threshold","type":"Integer","value":1,"constraints":["value >= 1","value <= 100"],"pathJava":"algorithmInstance.preprocessing.wordDfThreshold","pathRest":"preprocessing.wordDfThreshold","javadoc":{"text":"Word Document Frequency threshold. Words appearing in fewer than <code>dfThreshold</code>\\n documents will be ignored.","summary":"Word Document Frequency threshold."}}}}}},"queryHint":{"id":"queryHint","description":"Query hint","type":"String","value":null,"pathJava":"algorithmInstance.queryHint","pathRest":"queryHint","javadoc":{"text":"Query terms used to retrieve documents. The query is used as a hint to avoid trivial clusters.","summary":"Query terms used to retrieve documents."}},"useDimensionalityReduction":{"id":"useDimensionalityReduction","description":"Use dimensionality reduction","type":"Boolean","value":true,"pathJava":"algorithmInstance.useDimensionalityReduction","pathRest":"useDimensionalityReduction","javadoc":{"text":"If enabled, k-means will be applied on the dimensionality-reduced term-document matrix. The\\n number of dimensions will be equal to twice the number of requested clusters. If the number of\\n dimensions is lower than the number of input documents, reduction will not be performed. If\\n disabled, the k-means will be performed directly on the original term-document matrix.","summary":"If enabled, k-means will be applied on the dimensionality-reduced term-document matrix."}}}}')
}, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, , , , , function (e, t, r) {
}, , , , function (e, t, r) {
}, , , , , , , , , , , , , , , , , , , , , , , , , , , , function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, , function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, , function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
}, function (e, t, r) {
    "use strict";
    r.r(t);
    var a = r(0), n = r(1), i = r.n(n), s = r(30), o = r.n(s), c = (r(164), r(165), r(20)), l = r(11), u = r(22),
        d = r(52), h = r(21),
        m = [512, 512, 456, 512, 328, 456, 335, 512, 405, 328, 271, 456, 388, 335, 292, 512, 454, 405, 364, 328, 298, 271, 496, 456, 420, 388, 360, 335, 312, 292, 273, 512, 482, 454, 428, 405, 383, 364, 345, 328, 312, 298, 284, 271, 259, 496, 475, 456, 437, 420, 404, 388, 374, 360, 347, 335, 323, 312, 302, 292, 282, 273, 265, 512, 497, 482, 468, 454, 441, 428, 417, 405, 394, 383, 373, 364, 354, 345, 337, 328, 320, 312, 305, 298, 291, 284, 278, 271, 265, 259, 507, 496, 485, 475, 465, 456, 446, 437, 428, 420, 412, 404, 396, 388, 381, 374, 367, 360, 354, 347, 341, 335, 329, 323, 318, 312, 307, 302, 297, 292, 287, 282, 278, 273, 269, 265, 261, 512, 505, 497, 489, 482, 475, 468, 461, 454, 447, 441, 435, 428, 422, 417, 411, 405, 399, 394, 389, 383, 378, 373, 368, 364, 359, 354, 350, 345, 341, 337, 332, 328, 324, 320, 316, 312, 309, 305, 301, 298, 294, 291, 287, 284, 281, 278, 274, 271, 268, 265, 262, 259, 257, 507, 501, 496, 491, 485, 480, 475, 470, 465, 460, 456, 451, 446, 442, 437, 433, 428, 424, 420, 416, 412, 408, 404, 400, 396, 392, 388, 385, 381, 377, 374, 370, 367, 363, 360, 357, 354, 350, 347, 344, 341, 338, 335, 332, 329, 326, 323, 320, 318, 315, 312, 310, 307, 304, 302, 299, 297, 294, 292, 289, 287, 285, 282, 280, 278, 275, 273, 271, 269, 267, 265, 263, 261, 259],
        p = [9, 11, 12, 13, 13, 14, 14, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 17, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24];

    function b() {
        this.r = 0, this.g = 0, this.b = 0, this.a = 0, this.next = null
    }

    var g = [["hsl(60,100%,95%)", "hsl(64,92%,86%)", "hsl(78,72%,79%)", "hsl(96,54%,71%)", "hsl(121,41%,62%)", "hsl(136,45%,46%)", "hsl(140,58%,33%)", "hsl(152,100%,20%)", "hsl(156,100%,14%)"], ["hsl(60,100%,95%)", "hsl(53,100%,87%)", "hsl(45,98%,78%)", "hsl(40,99%,65%)", "hsl(32,99%,58%)", "hsl(26,85%,50%)", "hsl(22,98%,40%)", "hsl(19,95%,31%)", "hsl(19,89%,21%)"]],
        j = (e, t) => {
            var r = e.clientWidth, a = e.clientHeight, n = .0625;
            e.width = r * n, e.height = a * n;
            var i = Math.sqrt(r * r + a * a), s = t.slice(0).reverse().reduce((function (e, n, s) {
                for (var o = 1 - s / t.length, c = 0; c < 3; c++) e.push({
                    x: .5 * r + .7 * r * (.5 - Math.random()),
                    y: .75 * a + .7 * a * (.5 - Math.random()),
                    r: .3 * i * o + .2 * i * o * (.5 - Math.random()),
                    color: {hex: n, a: 1 / 3 * (.7 + .2 * (.5 - Math.random()))}
                });
                return e
            }), []), o = e.getContext("2d");
            o.scale(n, n), o.fillStyle = t[t.length - 1], o.fillRect(0, 0, r, a), s.forEach((function (e) {
                o.save(), o.fillStyle = e.color.hex, o.globalAlpha = e.color.a, o.beginPath(), o.arc(e.x, 1.2 * a - e.y, e.r, 0, 2 * Math.PI), o.closePath(), o.fill(), o.restore()
            })), ((e, t) => {
                for (var r, a, n, i, s, o, c, l, u, d, h, g, j, f, x, v, O, y = e.getContext("2d"), w = e.width, S = e.height, F = y.getImageData(0, 0, w, S), C = F.data, k = t + t + 1, T = w - 1, L = S - 1, I = t + 1, z = I * (I + 1) / 2, q = new b, N = q, R = 1; R < k; R++) if (N = N.next = new b, R === I) var D = N;
                N.next = q;
                var P = null, M = null;
                i = n = 0;
                for (var E = m[t], A = p[t], B = 0; B < S; B++) {
                    h = g = j = s = o = c = 0, l = I * (f = C[n]), u = I * (x = C[n + 1]), d = I * (v = C[n + 2]), s += z * f, o += z * x, c += z * v, N = q;
                    for (var W = 0; W < I; W++) N.r = f, N.g = x, N.b = v, N = N.next;
                    for (var J = 1; J < I; J++) r = n + ((T < J ? T : J) << 2), s += (N.r = f = C[r]) * (O = I - J), o += (N.g = x = C[r + 1]) * O, c += (N.b = v = C[r + 2]) * O, h += f, g += x, j += v, N = N.next;
                    P = q, M = D;
                    for (var H = 0; H < w; H++) C[n] = s * E >> A, C[n + 1] = o * E >> A, C[n + 2] = c * E >> A, s -= l, o -= u, c -= d, l -= P.r, u -= P.g, d -= P.b, r = i + ((r = H + t + 1) < T ? r : T) << 2, s += h += P.r = C[r], o += g += P.g = C[r + 1], c += j += P.b = C[r + 2], P = P.next, l += f = M.r, u += x = M.g, d += v = M.b, h -= f, g -= x, j -= v, M = M.next, n += 4;
                    i += w
                }
                for (var V = 0; V < w; V++) {
                    g = j = h = o = c = s = 0, l = I * (f = C[n = V << 2]), u = I * (x = C[n + 1]), d = I * (v = C[n + 2]), s += z * f, o += z * x, c += z * v, N = q;
                    for (var U = 0; U < I; U++) N.r = f, N.g = x, N.b = v, N = N.next;
                    a = w;
                    for (var Q = 1; Q <= t; Q++) n = a + V << 2, s += (N.r = f = C[n]) * (O = I - Q), o += (N.g = x = C[n + 1]) * O, c += (N.b = v = C[n + 2]) * O, h += f, g += x, j += v, N = N.next, Q < L && (a += w);
                    n = V, P = q, M = D;
                    for (var _ = 0; _ < S; _++) C[r = n << 2] = s * E >> A, C[r + 1] = o * E >> A, C[r + 2] = c * E >> A, s -= l, o -= u, c -= d, l -= P.r, u -= P.g, d -= P.b, r = V + ((r = _ + I) < L ? r : L) * w << 2, s += h += P.r = C[r], o += g += P.g = C[r + 1], c += j += P.b = C[r + 2], P = P.next, l += f = M.r, u += x = M.g, d += v = M.b, h -= f, g -= x, j -= v, M = M.next, n += w
                }
                y.putImageData(F, 0, 0)
            })(e, Math.ceil(.5))
        }, f = g[Math.floor(Math.random() * g.length) % g.length], x = f[6], v = /hsl\((\d+),.*/.exec(x)[1];
    document.documentElement.style.setProperty("--backdrop-color-hue", v);
    var O = () => {
            var e = Object(n.useRef)(null), t = Object(n.useState)(!1), r = Object(h.a)(t, 2), i = r[0], s = r[1];
            return Object(n.useEffect)((() => {
                j(e.current, f), s(!0)
            }), [e, s]), Object(a.jsx)("canvas", {
                className: "Backdrop ".concat(i ? "" : " hidden"),
                ref: e,
                style: {opacity: i}
            })
        }, y = (r(203), r(31)), w = (r(204), r(49)), S = (r(207), r(208), r(4)), F = r(6), C = r.n(F),
        k = Object(S.e)((({isLoading: e}) => Object(a.jsx)("div", {
            className: C()("Loading", {visible: e()}),
            children: Object(a.jsx)("div", {className: "dot-bricks"})
        }))), T = r(5), L = r(8), I = e => {
            var t = Object(n.useState)(null), r = Object(h.a)(t, 2), a = r[0], i = r[1], s = e.loader;
            return Object(n.useEffect)((() => {
                s().then((e => i(e)))
            }), [s]), a ? Object(n.createElement)(a, e.props) : null
        };
    I.propTypes = {loader: r.n(L).a.func.isRequired};
    var z = r(14), q = (r(100), Object(S.e)((() => Object(a.jsxs)("div", {
        className: "VisualizationHints",
        children: [Object(a.jsx)("h4", {children: "Pie-chart interaction help"}), Object(a.jsx)("table", {children: Object(a.jsxs)("tbody", {children: [Object(a.jsxs)("tr", {children: [Object(a.jsx)("td", {children: "Click"}), Object(a.jsx)("td", {children: "Select or unselect group."})]}), Object(a.jsxs)("tr", {children: [Object(a.jsxs)("td", {children: [Object(a.jsx)("kbd", {children: "Ctrl"}), " + click"]}), Object(a.jsx)("td", {children: "Select or unselect multiple groups."})]}), Object(a.jsxs)("tr", {children: [Object(a.jsx)("td", {children: "Double click"}), Object(a.jsxs)("td", {children: ["Expand group for easier browsing.", Object(a.jsx)("br", {}), "Double click again to collapse."]})]})]})})]
    })))), N = Object(S.e)((() => Object(a.jsxs)("div", {
        className: "VisualizationHints",
        children: [Object(a.jsx)("h4", {children: "Treemap interaction help"}), Object(a.jsx)("table", {
            children: Object(a.jsxs)("tbody", {
                children: [Object(a.jsxs)("tr", {children: [Object(a.jsx)("td", {children: "Click"}), Object(a.jsx)("td", {children: "Select or unselect group."})]}), Object(a.jsxs)("tr", {
                    className: "separator",
                    children: [Object(a.jsxs)("td", {children: [Object(a.jsx)("kbd", {children: "Ctrl"}), " + click"]}), Object(a.jsx)("td", {children: "Select or unselect multiple groups."})]
                }), Object(a.jsxs)("tr", {children: [Object(a.jsx)("td", {children: "Double click"}), Object(a.jsx)("td", {children: "Zoom and open group for browsing."})]}), Object(a.jsxs)("tr", {
                    className: "separator",
                    children: [Object(a.jsxs)("td", {children: [Object(a.jsx)("kbd", {children: "Shift"}), " + double click"]}), Object(a.jsx)("td", {children: "Unzoom and close group."})]
                }), Object(a.jsxs)("tr", {children: [Object(a.jsx)("td", {children: "Click-and-hold"}), Object(a.jsx)("td", {children: "Open group for browsing."})]}), Object(a.jsxs)("tr", {
                    className: "separator",
                    children: [Object(a.jsxs)("td", {children: [Object(a.jsx)("kbd", {children: "Shift"}), " + click-and-hold"]}), Object(a.jsx)("td", {children: "Close group."})]
                }), Object(a.jsxs)("tr", {children: [Object(a.jsxs)("td", {children: ["Mouse wheel,", Object(a.jsx)("br", {}), "click and move"]}), Object(a.jsx)("td", {children: "Zoom in and out, pan around."})]}), Object(a.jsxs)("tr", {children: [Object(a.jsx)("td", {children: Object(a.jsx)("kbd", {children: "Esc"})}), Object(a.jsx)("td", {children: "Reset view: unzoom, close all groups."})]})]
            })
        })]
    }))), R = r(61), D = r(40), P = r(15), M = r(12);
    var E = (e, t, r) => {
        if (e) switch (r) {
            case"jpeg":
            default:
                !function (e, t) {
                    var r = "image/jpeg", a = window.getComputedStyle(e.get("element").parentElement.parentElement),
                        n = e.get("imageData", {format: r, pixelRatio: 2, backgroundColor: a.backgroundColor});
                    fetch("data:" + r + ";" + n).then((e => e.blob())).then((e => {
                        Object(R.saveAs)(e, Object(M.b)(t, "jpg"))
                    }))
                }(e, t);
                break;
            case"json":
                !function (e, t) {
                    var r = Object.assign({}, e.get());
                    delete r.element, Object(R.saveAs)(new Blob([JSON.stringify(r)], {type: "application/json"}), Object(M.b)(t, "json"))
                }(e, t)
        }
    }, A = e => Object(a.jsx)(D.a, {
        icon: Object(a.jsx)(P.a, {icon: l.u}),
        minimal: !0,
        onClick: t => E(e.implRef.current, e.fileNameSuffix, t.shiftKey ? "json" : "jpeg")
    }), B = Object(z.b)("resultListConfig", {
        showRank: !0,
        openInNewTab: !0,
        showClusters: !0,
        maxCharsPerResult: 400,
        maxResultsPerPage: 50
    }), W = Object(S.e)((({children: e}) => {
        var t = B;
        return Object(a.jsxs)(a.Fragment, {
            children: [Object(a.jsx)("h4", {children: "Result list appearance"}), e, Object(a.jsx)("hr", {}), Object(a.jsx)(D.n, {
                label: "Show search rank",
                checked: t.showRank,
                onChange: e => t.showRank = e.target.checked
            }), Object(a.jsx)(D.n, {
                label: "Show clusters to which results belong",
                checked: t.showClusters,
                onChange: e => t.showClusters = e.target.checked
            }), Object(a.jsx)(D.n, {
                label: "Open links in a new tab",
                checked: t.openInNewTab,
                onChange: e => t.openInNewTab = e.target.checked
            }), Object(a.jsx)(D.d, {
                inline: !0,
                label: "Max chars per result",
                labelFor: "max-chars-per-result",
                children: Object(a.jsx)(D.g, {
                    id: "max-chars-per-result",
                    min: 0,
                    value: t.maxCharsPerResult,
                    onValueChange: e => t.maxCharsPerResult = e,
                    majorStepSize: 200,
                    stepSize: 50,
                    minorStepSize: 10
                })
            })]
        })
    })), J = (r(215), r(41));
    var H = Object(S.e)((function (e) {
        var t = e.cluster, r = t.clusters || [], n = r.length > 0,
            i = "(".concat(t.size, " docs") + (n ? ", ".concat(r.length, " subclusters)") : ")"),
            s = t.labels.join(", "), o = e.clusterSelectionStore,
            c = C()("TopCluster", {"with-subclusters": n, selected: o.isSelected(t)});
        return Object(a.jsxs)("div", {
            className: c,
            onClick: () => o.toggleSelection(t),
            children: [Object(a.jsx)(P.a, {className: "icon", icon: l.q}), Object(a.jsx)("span", {
                className: "labels",
                children: s
            }), " ", Object(a.jsx)("span", {
                className: "meta",
                children: i
            }), Object(a.jsx)("div", {
                className: "subclusters",
                children: r.map((e => Object(a.jsx)(V, {cluster: e, clusterSelectionStore: o}, e.id)))
            })]
        })
    }));
    var V = Object(S.e)((function (e) {
            var t = e.cluster, r = t.labels.join(", "), n = "(".concat(t.size, ")"), i = "(".concat(t.size, " docs)"),
                s = e.clusterSelectionStore, o = C()("SubCluster", {selected: s.isSelected(t)});
            return Object(a.jsxs)("span", {
                className: o,
                onClick: e => {
                    e.stopPropagation(), s.toggleSelection(t)
                },
                children: [Object(a.jsxs)("span", {
                    className: "icon",
                    children: [Object(a.jsx)(P.a, {icon: l.m}), "\xa0"]
                }), Object(a.jsx)("span", {
                    className: "labels",
                    children: r
                }), "\xa0", Object(a.jsx)("span", {className: "meta", title: i, children: n}), " "]
            })
        })), U = Object(S.e)((e => {
            var t = e.store;
            return Object(a.jsxs)("div", {
                className: "pie-chart config",
                children: [Object(a.jsx)("h4", {children: "Pie-chart appearance"}), Object(a.jsx)(D.n, {
                    label: "Include results as leaf nodes",
                    checked: t.includeResults,
                    onChange: e => t.includeResults = e.target.checked
                })]
            })
        })), Q = (r(216), Object(S.e)((e => {
            var t = e.store;
            return Object(a.jsxs)("div", {
                className: "treemap config",
                children: [Object(a.jsx)("h4", {children: "Treemap appearance"}), Object(a.jsx)(D.d, {
                    label: "Layout",
                    inline: !0,
                    children: Object(a.jsxs)(D.l, {
                        onChange: e => t.layout = e.target.value,
                        selectedValue: t.layout,
                        children: [Object(a.jsx)(D.k, {
                            label: "Polygonal",
                            value: "relaxed"
                        }), Object(a.jsx)(D.k, {label: "Rectangular", value: "squarified"})]
                    })
                }), Object(a.jsx)(D.d, {
                    label: "Stacking",
                    inline: !0,
                    children: Object(a.jsxs)(D.l, {
                        onChange: e => t.stacking = e.target.value,
                        selectedValue: t.stacking,
                        children: [Object(a.jsx)(D.k, {
                            label: "Hierarchical",
                            value: "hierarchical"
                        }), Object(a.jsx)(D.k, {label: "Flattened", value: "flattened"})]
                    })
                }), Object(a.jsx)(D.n, {
                    label: "Include results as leaf nodes",
                    checked: t.includeResults,
                    onChange: e => t.includeResults = e.target.checked
                })]
            })
        }))), _ = r(26), G = (r(217), r(38)),
        K = e => e.visible ? Object(a.jsx)(a.Fragment, {children: e.content()}) : null, X = (e, t) => {
            var r = {};
            return e && (r.display = "none"), Object.assign(r, t)
        }, Y = (r(218), r(43)), Z = e => {
            var t = e.cluster, r = (t.clusters || []).length > 0, n = t.labels.join(", ");
            return Object(a.jsxs)("span", {
                className: "ClusterInSummary",
                onClick: t => {
                    t.preventDefault(), e.onClick && e.onClick()
                },
                children: [Object(a.jsx)(P.a, {
                    icon: r ? l.q : l.m,
                    className: "icon"
                }), " ", Object(a.jsx)("span", {className: "labels", children: n})]
            })
        }, $ = Object(S.e)((() => {
            var e, t = J.a.selected, r = J.c.visibleDocumentIds;
            if (M.f.error) e = Object(a.jsx)(a.Fragment, {children: "Search results could not be retrieved due to an error."}); else if (0 === r.size) {
                var n = M.f.searchResult.documents.length;
                e = n > 0 ? Object(a.jsxs)(a.Fragment, {children: ["All retrieved results (", n, ")"]}) : Object(a.jsx)(a.Fragment, {children: "No results to show"})
            } else if (1 === t.size) {
                var i = t.values().next().value;
                e = Object(a.jsxs)(a.Fragment, {children: [i.size, " results in ", Object(a.jsx)(Z, {cluster: i})]})
            } else e = t.size > 1 ? Object(a.jsxs)(a.Fragment, {children: [Object(Y.c)(r.size, "result"), " in ", t.size, " ", "clusters"]}) : Object(a.jsx)(a.Fragment, {children: Object(Y.c)(r.size, "result")});
            return Object(a.jsx)("div", {className: "ClusterSelectionSummary", children: e})
        })), ee = Object(S.e)((e => {
            var t = J.a;
            return Object(a.jsx)("div", {
                className: "ResultClusters",
                children: Object(a.jsx)("span", {
                    children: (e.result.clusters || []).map((e => Object(a.jsxs)(i.a.Fragment, {
                        children: [Object(a.jsx)(Z, {
                            cluster: e,
                            onClick: () => t.toggleSelection(e)
                        }), " "]
                    }, e.id)))
                })
            })
        })), te = Object(S.e)((e => {
            var t = e.document, r = e.children, n = e.visible, i = void 0 === n || n, s = B;
            return Object(a.jsxs)("a", {
                className: "Result",
                href: t.url,
                target: s.openInNewTab ? "_blank" : "_self",
                rel: "noopener noreferrer",
                style: {display: i ? "block" : "none"},
                children: [r, Object(a.jsx)(K, {visible: s.showClusters, content: () => Object(a.jsx)(ee, {result: t})})]
            })
        })), re = Object(S.e)((e => {
            var t = e.document, r = e.source, n = e.visible, i = void 0 === n || n;
            return Object(a.jsx)(te, {document: t, visible: i, children: r.createResult(e)})
        })), ae = Object(S.e)((e => {
            var t = e.document, r = e.visibilityStore, n = r.allDocumentsVisible || r.isVisible(t);
            return Object(a.jsx)(re, Object(T.a)(Object(T.a)({}, e), {}, {visible: n}))
        })), ne = ({
                       enabled: e,
                       start: t,
                       end: r,
                       total: n,
                       next: i,
                       prev: s,
                       nextEnabled: o,
                       prevEnabled: c
                   }) => e ? Object(a.jsxs)("div", {
            className: "ResultListPaging",
            children: [Object(a.jsx)(G.a, {
                enabled: c,
                onClick: s,
                children: "< Previous"
            }), Object(a.jsxs)("span", {children: [t + 1, " \u2014 ", r, " of ", n]}), Object(a.jsx)(G.a, {
                enabled: o,
                onClick: i,
                children: "Next >"
            })]
        }) : null, ie = Object(S.e)((e => {
            var t, r, i = e.store, s = i.searchResult.documents, o = s.length > 200;
            o ? (r = re, t = e.visibilityStore.allDocumentsVisible ? s : s.filter((t => e.visibilityStore.isVisible(t)))) : (r = ae, t = s);
            var c, l = (() => {
                    var e = Object(n.useRef)(void 0), t = Object(n.useCallback)((() => {
                        e.current && (e.current.scrollTop = 0)
                    }), []);
                    return {container: e, scrollReset: t}
                })(), u = l.container, d = l.scrollReset, h = (({enabled: e, maxPerPage: t, results: r, onChange: a}) => {
                    var i = Object(S.d)({start: 0}), s = Object(n.useCallback)((() => {
                        i.start = 0
                    }), [i]), o = i.start, c = o + t;
                    return {
                        end: c, start: o, total: r.length, results: e ? r.slice(o, c) : r, next: () => {
                            i.start = c, a()
                        }, prev: () => {
                            i.start = o - t, a()
                        }, nextEnabled: c < r.length, prevEnabled: o > 0, enabled: e && r.length > t, reset: s
                    }
                })({enabled: o, maxPerPage: B.maxResultsPerPage, results: t, onChange: d}), m = h.results, p = h.reset,
                b = Object(_.a)(h, ["results", "reset"]), g = Object(n.useCallback)((() => {
                    d(), p()
                }), [p, d]);
            c = g, Object(n.useEffect)((() => {
                var e = () => {
                    J.a.selected.size >= 0 && c()
                };
                return Object(S.a)(e), () => Object(S.c)(e)
            }), [c]);
            var j = e.limit ? m.slice(0, 5) : m;
            return Object(a.jsx)("div", {
                className: "ResultList",
                ref: u,
                children: Object(a.jsxs)("div", {
                    children: [Object(a.jsx)($, {}), j.map(((t, n) => Object(a.jsx)(r, {
                        document: t,
                        source: i.searchResult.source,
                        rank: n + 1,
                        visibilityStore: e.visibilityStore
                    }, n))), Object(a.jsx)(ne, Object(T.a)({}, b))]
                })
            })
        })), se = e => {
            var t = Object(n.useState)(!0), r = Object(h.a)(t, 2), i = r[0], s = r[1];
            return Object(n.useEffect)((() => {
                setTimeout((() => {
                    s(!1)
                }), 100)
            }), [s]), Object(a.jsx)(ie, Object(T.a)(Object(T.a)({}, e), {}, {limit: i}))
        }, oe = Object(S.e)((() => {
            var e = M.d.clusters, t = e.reduce(((e, t) => e && (!t.clusters || 0 === t.clusters.length)), !0);
            return Object(a.jsx)("div", {
                className: "ClusterList" + (t ? " flat" : ""),
                children: Object(a.jsx)("div", {
                    children: e.length > 0 ? e.map((e => Object(a.jsx)(H, {
                        cluster: e,
                        clusterSelectionStore: J.a
                    }, e.id))) : Object(a.jsx)("div", {children: "No clusters to show"})
                })
            })
        })), ce = Object(z.b)("treemapConfig", {layout: "relaxed", stacking: "hierarchical", includeResults: !0}),
        le = Object(z.b)("pieChartConfig", {includeResults: !0}), ue = () => {
            var e = Object(S.d)({loading: !1}), t = {
                current: void 0, setCurrent: r => {
                    t.current = r, r.set("onRolloutStart", (() => e.loading = !1))
                }, isLoading: () => e.loading
            };
            return Object(S.a)((() => {
                M.d.clusters.length > 0 && (e.loading = !0)
            })), t
        }, de = ue(), he = ue(),
        me = () => Promise.all([r.e(12), r.e(8)]).then(r.bind(null, 276)).then((e => Object(S.e)(e.Treemap))),
        pe = () => Promise.all([r.e(11), r.e(4)]).then(r.bind(null, 277)).then((e => Object(S.e)(e.PieChart))), be = [{
            label: "Clusters", views: {
                folders: {label: "list", createContentElement: e => Object(a.jsx)(oe, Object(T.a)({}, e)), tools: []},
                treemap: {
                    label: "treemap",
                    isLoading: de.isLoading,
                    createContentElement: e => {
                        var t = {visible: e, configStore: ce, implRef: de};
                        return Object(a.jsx)(I, {loader: me, props: t})
                    },
                    tools: [{
                        id: "interaction",
                        icon: l.t,
                        createContentElement: e => Object(a.jsx)(N, {}),
                        title: "Treemap interaction help"
                    }, {
                        id: "export-image",
                        createContentElement: e => Object(a.jsx)(A, {implRef: de, fileNameSuffix: "treemap"}),
                        title: "Export treemap as JPEG"
                    }, {
                        id: "config",
                        icon: l.f,
                        createContentElement: e => Object(a.jsx)(Q, {store: ce}),
                        title: "Treemap settings"
                    }]
                },
                "pie-chart": {
                    label: "pie-chart",
                    isLoading: he.isLoading,
                    createContentElement: e => {
                        var t = {visible: e, configStore: le, implRef: he};
                        return Object(a.jsx)(I, {loader: pe, props: t})
                    },
                    tools: [{
                        id: "interaction",
                        icon: l.t,
                        createContentElement: e => Object(a.jsx)(q, {})
                    }, {
                        id: "export-image",
                        createContentElement: e => Object(a.jsx)(A, {implRef: he, fileNameSuffix: "pie-chart"}),
                        title: "Export pie-chart as JPEG"
                    }, {id: "config", icon: l.f, createContentElement: e => Object(a.jsx)(U, {store: le})}]
                }
            }
        }], ge = [{
            label: "Results",
            views: {
                list: {
                    label: "list",
                    createContentElement: e => Object(a.jsx)(se, Object(T.a)(Object(T.a)({}, e), {}, {
                        store: M.f,
                        visibilityStore: J.c,
                        clusterSelectionStore: J.a
                    })),
                    tools: [{
                        id: "config",
                        icon: l.f,
                        createContentElement: e => Object(a.jsx)(W, {children: e.source.createConfig()})
                    }]
                }
            }
        }], je = r(28), fe = (r(219), r(13));

    function xe(e, t) {
        var r = "https://www.etools.ch/partnerSearch.do?" + new URLSearchParams(Object.assign({
            partner: "Carrot2Json",
            query: e,
            dataSourceResults: 40,
            maxRecords: 200
        }, t));
        return window.fetch(r).catch((e => ({statusText: Object(Y.a)("Failed to connect to eTools service at ".concat(r, ": ").concat(e.message))}))).then((function (e) {
            if (!e.ok) throw e;
            return e.json()
        }))
    }

    var ve = e => Object(a.jsxs)("strong", {
            children: [Object(a.jsx)(K, {
                visible: e.showRank,
                content: () => Object(a.jsx)("span", {children: e.rank})
            }), e.title]
        }), Oe = e => Object(a.jsx)("span", {className: "url", children: Object(a.jsx)("span", {children: e.url})}),
        ye = Object(z.b)("workbench:query", {query: ""}), we = r(32),
        Se = Object(z.b)("etoolsResultConfig", {showSiteIcons: !1, showSources: !0}),
        Fe = Object(z.b)("etoolsSourceConfig", {
            safeSearch: !0,
            dataSources: "all",
            language: "en",
            country: "web",
            partner: "Carrot2Json",
            customerId: ""
        }), Ce = [{label: "All", value: "all"}, {label: "Fastest", value: "fastest"}],
        ke = [{value: "web", label: "All"}, {value: "AT", label: "Austria"}, {
            value: "FR",
            label: "France"
        }, {value: "DE", label: "Germany"}, {value: "GB", label: "Great Britain"}, {
            value: "IT",
            label: "Italy"
        }, {value: "LI", label: "Lichtenstein"}, {value: "ES", label: "Spain"}, {value: "CH", label: "Switzerland"}],
        Te = [{value: "all", label: "All"}, {value: "en", label: "English"}, {
            value: "fr",
            label: "French"
        }, {value: "de", label: "German"}, {value: "it", label: "Italian"}, {value: "es", label: "Spanish"}], Le = [{
            id: "web",
            type: "group",
            label: "Web",
            settings: [Object(T.a)(Object(T.a)({id: "web:query"}, Object(fe.e)(ye, "query")), {}, {
                type: "string",
                label: "Query",
                description: "\n<p>\n  The search query to pass to eTools. Use the common web search engine syntax: double quotes\n  for phrase search, <code>-</code> to exclude words or phrases etc.\n</p>"
            }), Object(T.a)(Object(T.a)({id: "web:language"}, Object(fe.e)(Fe, "language")), {}, {
                type: "enum",
                ui: "select",
                label: "Language",
                options: Te,
                description: "\n<p>\n  Restricts the search results to a specific language.\n</p>"
            }), Object(T.a)(Object(T.a)({id: "web:country"}, Object(fe.e)(Fe, "country")), {}, {
                type: "enum",
                ui: "select",
                label: "Country",
                options: ke,
                description: "\n<p>\n  Restricts the search results to websites from a specific country.\n</p>"
            }), Object(T.a)(Object(T.a)({id: "web:safeSearch"}, Object(fe.e)(Fe, "safeSearch")), {}, {
                type: "boolean",
                label: "Safe search",
                description: "\n<p>\n  Controls filtering of offensive search results.\n</p>"
            }), Object(T.a)(Object(T.a)({id: "web:dataSources"}, Object(fe.e)(Fe, "dataSources")), {}, {
                type: "enum",
                ui: "radio",
                inline: !0,
                label: "Data sources",
                advanced: !0,
                options: Ce,
                description: "\n<p>\n  Determines the set of search engines from which to aggregate the results.\n</p>"
            }), Object(T.a)(Object(T.a)({id: "web:partner"}, Object(fe.e)(Fe, "partner")), {}, {
                type: "string",
                label: "Partner",
                advanced: !0,
                description: "\n<p>\n  If you have a custom service agreement with eTools, provide your partner ID here.  \n</p>"
            }), Object(T.a)(Object(T.a)({id: "web:customerId"}, Object(fe.e)(Fe, "customerId")), {}, {
                type: "string",
                label: "Customer ID",
                advanced: !0,
                description: "\n<p>\n  Customer ID, optional. If you have a custom service agreement with eTools, provide your customer ID here.  \n</p>"
            })]
        }], Ie = Object(S.e)((e => {
            var t = e.document, r = new URL(window.location).protocol,
                n = new URL(t.url.startsWith("//") ? r + t.url : t.url).hostname, i = Se, s = B, o = null;
            o = i.showSiteIcons ? Object(a.jsx)("span", {
                className: "url with-site-icon",
                style: {backgroundImage: "url(".concat(r, "//").concat(n + "/favicon.ico", ")")},
                children: Object(a.jsx)("span", {children: t.url})
            }) : Object(a.jsx)(Oe, {url: t.url});
            var c, l = s.maxCharsPerResult;
            return c = 0 === l ? null : t.snippet && t.snippet.length > l ? t.snippet.substring(0, l) + "\u2026" : t.snippet, Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)(ve, {
                    title: t.title,
                    rank: e.rank,
                    showRank: s.showRank
                }), Object(a.jsx)("div", {children: c}), o, Object(a.jsx)(K, {
                    visible: i.showSources,
                    content: () => Object(a.jsx)("div", {
                        className: "sources",
                        children: t.sources.map(((e, t) => Object(a.jsx)("span", {children: e}, t)))
                    })
                })]
            })
        })), ze = Object(S.e)((() => {
            var e = Se;
            return Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)(D.n, {
                    label: "Show site icons",
                    checked: e.showSiteIcons,
                    onChange: t => e.showSiteIcons = t.target.checked
                }), Object(a.jsx)(D.n, {
                    label: "Show sources",
                    checked: e.showSources,
                    onChange: t => e.showSources = t.target.checked
                })]
            })
        })), qe = Object(S.d)({detailsVisible: !1}), Ne = Object(S.e)((e => {
            var t = Fe, r = () => {
                e.onChange && e.onChange()
            };
            return Object(a.jsxs)("div", {
                className: "EToolsAccessDetails",
                children: [Object(a.jsx)("h4", {children: "eTools access tokens"}), Object(a.jsx)(D.d, {
                    label: "Partner ID",
                    labelFor: "partner-id",
                    inline: !0,
                    children: Object(a.jsx)(D.f, {
                        id: "partner-id",
                        value: t.partner,
                        onChange: e => (r(), t.partner = e.target.value)
                    })
                }), Object(a.jsx)(D.d, {
                    label: "Customer ID",
                    labelInfo: "(optional)",
                    labelFor: "customer-id",
                    inline: !0,
                    children: Object(a.jsx)(D.f, {
                        id: "customer-id",
                        value: t.customerId,
                        onChange: e => (r(), t.customerId = e.target.value)
                    })
                })]
            })
        })), Re = e => {
            var t = qe;
            return Object(a.jsx)(G.a, {
                onClick: e => {
                    e.preventDefault(), t.detailsVisible = !t.detailsVisible
                }, children: e.children
            })
        }, De = Object(S.e)((e => {
            var t = qe.detailsVisible;
            return Object(a.jsxs)("div", {
                style: {display: t ? "block" : "none", marginTop: "2em"},
                children: [Object(a.jsx)(Ne, {onChange: e.onChange}), e.children]
            })
        })), Pe = () => Object(a.jsx)("a", {
            href: "https://etools.ch",
            target: "_blank",
            rel: "noopener noreferrer",
            children: "eTools"
        }), Me = Object(S.e)((e => {
            var t = Fe;
            return Object(a.jsxs)("div", {
                className: "EToolsSourceConfig",
                children: [Object(a.jsx)(D.d, {
                    label: "Language",
                    labelFor: "etools-language",
                    inline: !0,
                    children: Object(a.jsx)(D.e, {
                        onChange: r => {
                            t.language = r.currentTarget.value, e.onChange()
                        },
                        id: "etools-language",
                        value: t.language,
                        children: Te.map((e => Object(a.jsx)("option", {value: e.value, children: e.label}, e.value)))
                    })
                }), Object(a.jsx)(D.d, {
                    label: "Country",
                    labelFor: "etools-country",
                    inline: !0,
                    children: Object(a.jsx)(D.e, {
                        onChange: r => {
                            t.country = r.currentTarget.value, e.onChange()
                        },
                        id: "etools-country",
                        value: t.country,
                        children: ke.map((e => Object(a.jsx)("option", {value: e.value, children: e.label}, e.value)))
                    })
                }), Object(a.jsx)(D.d, {
                    inline: !0,
                    label: "Sources",
                    labelFor: "etools-sources",
                    children: Object(a.jsx)(D.l, {
                        onChange: r => {
                            t.dataSources = r.currentTarget.value, e.onChange()
                        },
                        selectedValue: t.dataSources,
                        id: "etools-sources",
                        inline: !0,
                        children: Ce.map((e => Object(a.jsx)(D.k, Object(T.a)({}, e), e.value)))
                    })
                }), Object(a.jsx)(D.d, {
                    inline: !0,
                    label: " ",
                    children: Object(a.jsx)(D.n, {
                        label: "Safe search", checked: t.safeSearch, onChange: r => {
                            t.safeSearch = r.target.checked, e.onChange()
                        }
                    })
                }), Object(a.jsx)("p", {children: Object(a.jsxs)("small", {children: ["Web search feed is kindly provided to us by ", Object(a.jsx)(Pe, {}), ". If you have custom eTools access tokens,", " ", Object(a.jsx)(Re, {children: "provide them here"}), "."]})}), Object(a.jsx)(De, {onChange: e.onChange})]
            })
        })), Ee = Object(S.e)((() => Object(a.jsxs)("div", {
            className: "Error",
            children: [Object(a.jsx)("h3", {children: "Search limit exceeded"}), Object(a.jsxs)("p", {children: [Object(a.jsx)(Pe, {}), ", our web search results provider, blocked access to the service due automated querying or excessive number of searches issued from your IP address."]}), Object(a.jsxs)("p", {
                children: ["The block may be lifted after some time, but if you keep seeing this message, you may need to", " ", Object(a.jsx)("a", {
                    href: "mailto:sschmid@comcepta.com",
                    target: "_blank",
                    rel: "noopener noreferrer",
                    children: "contact eTools"
                }), " ", "to arrange for an unlimited search service."]
            }), Object(a.jsxs)("p", {children: ["Once you get your eTools access tokens,", " ", Object(a.jsx)(Re, {children: "provide them here"}), "."]}), Object(a.jsx)(De, {
                children: Object(a.jsx)(D.a, {
                    onClick: () => document.location.reload(),
                    intent: "primary",
                    children: "Apply and re-run search"
                })
            })]
        }))),
        Ae = () => Object(a.jsxs)(a.Fragment, {children: ["Type your query in the ", Object(a.jsx)("strong", {children: "Query"}), " box. Use the common web search engine syntax such as double quotes for", " ", Object(a.jsx)("code", {children: '"phrase search"'}), ",", Object(a.jsx)("code", {children: "-"}), " to exclude words or phrases etc."]}),
        Be = {
            label: "Web",
            descriptionHtml: "web search results provided by <a href='https://etools.ch' target='_blank'>etools.ch</a>. Extensive use may require special arrangements with the <a href='mailto:sschmid@comcepta.com' target='_blank'>owner</a> of the etools.ch service.",
            contentSummary: "Web search results",
            source: e => {
                var t = Fe;
                return function (e, t) {
                    return xe(e, t).then((function (e) {
                        return {
                            query: e.request.query,
                            matches: e.response.totalEstimatedRecords,
                            documents: e.response.mergedRecords.map(((e, t) => ({
                                id: t.toString(),
                                title: e.title,
                                snippet: e.text,
                                url: e.url,
                                sources: e.sources
                            })))
                        }
                    }))
                }(e, {safeSearch: t.safeSearch, dataSources: t.dataSources, language: t.language, country: t.country})
            },
            createResult: e => Object(a.jsx)(Ie, Object(T.a)({}, e)),
            createError: e => e && 403 === e.status ? Object(a.jsx)(Ee, {}) : Object(a.jsx)(we.a, {}),
            createConfig: () => Object(a.jsx)(ze, {}),
            createSourceConfig: e => Object(a.jsx)(Me, Object(T.a)({}, e)),
            getSettings: () => Le,
            getFieldsToCluster: () => ["title", "snippet"],
            createIntroHelp: () => Object(a.jsx)(Ae, {})
        };
    r(220);

    function We(e) {
        var t = (new DOMParser).parseFromString(e, "application/xml"), r = t.createNSResolver(t);
        this.getNodes = (e, a = t) => {
            for (var n, i = t.evaluate(e, a, r, XPathResult.ANY_TYPE, null), s = []; n = i.iterateNext();) s.push(n);
            return s
        }, this.getString = (e, a = t) => t.evaluate(e, a, r, XPathResult.STRING_TYPE, null).stringValue, this.getStrings = (e, r = t) => this.getNodes(e, r).map((e => e.textContent))
    }

    var Je = (e, t) => (t.apiKey && t.apiKey.length > 0 && (e.api_key = t.apiKey), e);

    function He(e, t) {
        var r = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + new URLSearchParams(Je({
            db: "pubmed",
            term: e,
            retmax: t.maxResults,
            retmode: "json"
        }, t));
        return window.fetch(r).catch((e => ({statusText: "Failed to connect to PubMed service at ".concat(r, ": ").concat(e.message, ".")}))).then((e => {
            if (!e.ok) throw e;
            return e.json()
        }))
    }

    function Ve(e, t) {
        var r = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + new URLSearchParams(Je({
            db: "pubmed",
            retmode: "xml"
        }, t));
        return window.fetch(r, {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: "id=" + e.join(",")
        }).catch((e => ({statusText: "Failed to connect to PubMed service at ".concat(r.substring(0, 100) + "...", ": ").concat(e.message, ".")}))).then((e => {
            if (!e.ok) throw e;
            return e.text()
        }))
    }

    var Ue, Qe = Object(z.b)("pubmedResultConfig", {showJournal: !0, showKeywords: !0}),
        _e = Object(z.b)("pubmedSourceResultConfig", {maxResults: 100, apiKey: ""}), Ge = [{
            id: "pubmed",
            type: "group",
            label: "PubMed",
            settings: [{
                id: "pubmed:query",
                get: () => ye.query,
                set: (e, t) => ye.query = t,
                type: "string",
                label: "Query",
                description: "<p>The search query to pass to PubMed.</p>"
            }, {
                id: "pubmed:maxResults",
                get: () => _e.maxResults,
                set: (e, t) => _e.maxResults = t,
                type: "number",
                label: "Max results",
                min: 0,
                max: 500,
                step: 10,
                description: "<p>The number of search results to fetch.</p>"
            }, {
                id: "pubmed:apiKey",
                get: () => _e.apiKey,
                set: (e, t) => _e.apiKey = t,
                type: "string",
                label: "API key",
                description: '<p><a href="https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/" target=_blank>PubMed API key</a>, optional.</p>'
            }]
        }], Ke = Object(S.e)((e => {
            var t = e.document, r = B, n = Qe, i = null;
            r.showRank && (i = Object(a.jsx)("span", {children: e.rank}));
            var s = r.maxCharsPerResult;
            return Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)(ve, {
                    title: t.title,
                    rank: i,
                    showRank: r.showRank
                }), Object(a.jsx)(K, {
                    visible: n.showJournal,
                    content: () => Object(a.jsxs)("div", {children: [t.journal, ", ", t.year]})
                }), Object(a.jsx)("div", {
                    children: (t.paragraphs || []).map((() => {
                        var e = 0;
                        return (t, r) => {
                            return 0 === s || e + 80 >= s ? null : (n = e + t.text.length < s ? t.text : t.text.substring(0, s - e) + "\u2026", e += n.length, Object(a.jsxs)("p", {
                                children: [Object(a.jsx)(K, {
                                    visible: !!t.label,
                                    content: () => Object(a.jsx)("span", {children: t.label})
                                }), n]
                            }, r));
                            var n
                        }
                    })())
                }), Object(a.jsx)(K, {
                    visible: n.showKeywords && t.keywords && t.keywords.length > 0,
                    content: () => Object(a.jsxs)("div", {
                        className: "keywords",
                        children: [Object(a.jsx)("span", {children: "Keywords"}), t.keywords.join(", ")]
                    })
                }), Object(a.jsx)(Oe, {url: t.url})]
            })
        })), Xe = Object(S.e)((() => {
            var e = Qe;
            return Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)(D.n, {
                    label: "Show journal",
                    checked: e.showJournal,
                    onChange: t => e.showJournal = t.target.checked
                }), Object(a.jsx)(D.n, {
                    label: "Show keywords",
                    checked: e.showKeywords,
                    onChange: t => e.showKeywords = t.target.checked
                })]
            })
        })), Ye = Object(S.e)((e => {
            var t = _e;
            return Object(a.jsxs)("div", {
                className: "PubMedSourceConfig",
                children: [Object(a.jsx)(D.d, {
                    inline: !0,
                    label: "Max results",
                    labelFor: "pubmed-max-results",
                    children: Object(a.jsx)(D.g, {
                        id: "pubmed-max-results",
                        min: 50,
                        max: 1e3,
                        value: t.maxResults,
                        onValueChange: r => {
                            t.maxResults = r, e.onChange()
                        },
                        majorStepSize: 100,
                        stepSize: 50,
                        minorStepSize: 10,
                        clampValueOnBlur: !0
                    })
                }), Object(a.jsx)(D.d, {
                    inline: !0,
                    label: "API key",
                    labelFor: "pubmed-api-key",
                    children: Object(a.jsx)(D.f, {
                        id: "pubmed-api-key", value: t.apiKey, onChange: r => {
                            t.apiKey = r.target.value.trim(), e.onChange()
                        }
                    })
                })]
            })
        })), Ze = () => Object(a.jsxs)(a.Fragment, {
            children: [Object(a.jsxs)("p", {children: ["Type your PubMed query in the ", Object(a.jsx)("strong", {children: "Query"}), " box."]}), Object(a.jsxs)("p", {
                children: ["To request larger numbers of PubMed results, you may need to get the", " ", Object(a.jsx)("a", {
                    href: "https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/",
                    children: "NCBI API key"
                }), " ", "and provide it in the ", Object(a.jsx)("strong", {children: "API key"}), " field."]
            })]
        }), $e = {
            label: "PubMed",
            descriptionHtml: "abstracts of medical papers from the PubMed database provided by NCBI.",
            contentSummary: "PubMed abstracts",
            source: e => function (e, t) {
                var r = Ve;
                return He(e, t).then((e => r(e.esearchresult.idlist, t))).then((t => {
                    var r = new We(t), a = r.getNodes("//PubmedArticle").map((e => {
                        var t = r.getString(".//PMID", e), a = r.getNodes(".//AbstractText", e).map((e => ({
                            label: e.getAttribute("Label"),
                            text: e.textContent.replace("\u2003", "")
                        })));
                        return {
                            id: t,
                            title: r.getString(".//ArticleTitle", e),
                            snippet: a.map((e => e.text)).join(" "),
                            paragraphs: a,
                            journal: r.getString(".//Journal/Title", e),
                            year: r.getString(".//Journal//Year", e),
                            keywords: r.getStrings(".//Keyword", e),
                            url: "https://www.ncbi.nlm.nih.gov/pubmed/".concat(t)
                        }
                    }));
                    return {query: e, matches: a.length, documents: a}
                }))
            }(e, {maxResults: _e.maxResults, apiKey: _e.apiKey}),
            createResult: e => Object(a.jsx)(Ke, Object(T.a)({}, e)),
            createError: e => Object(a.jsx)(we.a, Object(T.a)({}, e)),
            createConfig: () => Object(a.jsx)(Xe, {}),
            createSourceConfig: e => Object(a.jsx)(Ye, Object(T.a)({}, e)),
            getSettings: () => Ge,
            getFieldsToCluster: () => ["title", "snippet"],
            createIntroHelp: () => Object(a.jsx)(Ze, {})
        }, et = r(7), tt = r.n(et), rt = r(16), at = (r(221), r(113)), nt = r.n(at), it = ({jsonString: e}) => {
            var t = nt()(e, {
                keyColor: "prop",
                numberColor: "number",
                stringColor: "string",
                trueColor: "true",
                falseColor: "false",
                nullColor: "null"
            });
            return Object(a.jsx)("pre", {className: "JsonHighlighted", dangerouslySetInnerHTML: {__html: t}})
        }, st = (r(222), r(44)), ot = r(45), ct = e => {
            var t = e => e.join("--"), r = Object(S.d)({
                    fieldRoles: {},
                    resultForPreview: void 0,
                    maxPropertyValuesToShow: 3,
                    maxTagValuesToShow: 8,
                    isEmpty: () => 0 === Object.keys(r.fieldRoles).length,
                    load: (e, n) => {
                        if (0 !== e.length) {
                            var i = a.get(t(e.map((e => e.field))));
                            if (!i) {
                                i = e.reduce(((e, t) => (t.tagScore > 1 && t.tagScore > t.propScore ? e[t.field] = "tag" : t.propScore > 1 && t.propScore > t.tagScore && t.distinct > 1 ? e[t.field] = "property" : t.naturalTextScore >= 8 ? e[t.field] = "body" : e[t.field] = "not shown", e)), {});
                                var s = e.sort(((e, t) => t.idScore - e.idScore));
                                s[0].idScore >= 2 && (i[s[0].field] = "id");
                                var o = e.sort(((e, t) => t.titleScore - e.titleScore));
                                o[0].titleScore >= 2 && (i[o[0].field] = "title")
                            }
                            r.fieldRoles = i, r.resultForPreview = n.documents.find((e => Object.keys(e).reduce(((t, r) => t && !Object(st.d)(e[r])), !0) || n.documents[0]))
                        }
                    }
                }),
                a = Object(z.a)("workbench:source:".concat(e, ":resultConfigs"), (e => t(Object.keys(e))), (() => r.fieldRoles));
            return r
        }, lt = ["not shown", "title", "body", "tag", "property", "id"], ut = Object(S.e)((({field: e, configStore: t}) => {
            var r = t.fieldRoles[e];
            return Object(a.jsx)(D.d, {
                label: Object(a.jsxs)(a.Fragment, {children: [Object(a.jsx)("span", {children: e}), Object(a.jsx)("small", {children: "show as"})]}),
                inline: !0,
                children: Object(a.jsx)(D.e, {
                    value: r,
                    className: "not shown" === r ? "empty" : null,
                    onChange: r => t.fieldRoles[e] = r.currentTarget.value,
                    children: lt.map((e => Object(a.jsx)("option", {value: e, children: e}, e)))
                })
            })
        })), dt = ({configStore: e}) => Object(a.jsx)("div", {
            className: "FieldRoles",
            children: Object.keys(e.fieldRoles).sort().map((t => Object(a.jsx)(ut, {field: t, configStore: e}, t)))
        }), ht = Object(S.e)((({configStore: e}) => {
            var t = e.resultForPreview, r = t ? Object(a.jsx)(te, {
                document: t,
                children: Object(a.jsx)(bt, {document: t, rank: 1, configStore: e})
            }) : Object(a.jsx)("span", {children: "Not available"});
            return Object(a.jsxs)("div", {
                children: [Object(a.jsx)("p", {children: "Preview:"}), Object(a.jsx)("div", {
                    className: "ResultPreview",
                    children: r
                })]
            })
        })), mt = Object(S.e)((({configStore: e}) => Object(a.jsxs)("div", {
            className: "FieldConfigs",
            children: [Object(a.jsx)(D.d, {
                inline: !0,
                label: "Max property values",
                labelFor: "max-property-values",
                children: Object(a.jsx)(D.g, {
                    id: "max-property-values",
                    min: 1,
                    value: e.maxPropertyValuesToShow,
                    onValueChange: t => e.maxPropertyValuesToShow = t,
                    majorStepSize: 5,
                    stepSize: 1,
                    minorStepSize: 1
                })
            }), Object(a.jsx)(D.d, {
                inline: !0,
                label: "Max tag values",
                labelFor: "max-tag-values",
                children: Object(a.jsx)(D.g, {
                    id: "max-tag-values",
                    min: 1,
                    value: e.maxTagValuesToShow,
                    onValueChange: t => e.maxTagValuesToShow = t,
                    majorStepSize: 5,
                    stepSize: 1,
                    minorStepSize: 1
                })
            })]
        }))), pt = Object(S.e)((({configStore: e}) => Object(a.jsxs)("div", {
            className: "CustomSchemeResultConfig",
            style: X(e.isEmpty()),
            children: [Object(a.jsxs)("div", {
                className: "main",
                children: [Object(a.jsxs)("div", {children: [Object(a.jsx)("p", {children: "Choose the fields to show:"}), Object(a.jsx)(dt, {configStore: e})]}), Object(a.jsx)(ht, {configStore: e})]
            }), Object(a.jsx)(mt, {configStore: e})]
        }))), bt = Object(S.e)((({document: e, rank: t, configStore: r}) => {
            var n = r.fieldRoles, s = Object.keys(n).reduce(((e, t) => {
                var r = n[t];
                return "not shown" !== r && e[r].push(t), e
            }), {title: [], body: [], tag: [], property: [], id: []}), o = s.body.reduce(((t, r) => {
                var a = e[r];
                a && Object(ot.c)(a).forEach(((e, a) => {
                    0 === a ? t.push({text: e, field: r}) : t.push({text: e})
                }));
                return t
            }), []), c = s.property.reduce(((t, a) => {
                var n = Object(ot.c)(e[a]).reduce(((e, t) => (e.length < r.maxPropertyValuesToShow && !Object(st.d)(t) && e.push(t), e)), []);
                return n.length > 0 && t.push({field: a, text: n.join(", ")}), t
            }), []);
            return Object(a.jsxs)(a.Fragment, {
                children: [s.title.map(((r, n) => Object(a.jsx)(ve, {
                    title: Object(ot.c)(e[r]).join(", "),
                    rank: t,
                    showRank: 0 === n && B.showRank
                }, r))), Object(a.jsx)("div", {
                    children: Object(ot.b)(o, B.maxCharsPerResult, ((e, t, r) => {
                        var n = t.field ? Object(a.jsx)("span", {children: t.field}) : null;
                        return Object(a.jsxs)("p", {children: [n, e]}, r)
                    }), (e => e.text))
                }), [...s.id, ...s.tag].map((t => {
                    var n = Object(ot.c)(e[t]).slice(0, r.maxTagValuesToShow);
                    return Object(a.jsxs)("div", {
                        className: "tags",
                        children: [Object(a.jsx)("span", {children: t}), n.join(", ")]
                    }, t)
                })), Object(a.jsx)("dl", {
                    className: "properties",
                    children: c.map((e => Object(a.jsxs)(i.a.Fragment, {children: [Object(a.jsx)("dt", {children: e.field}), Object(a.jsx)("dd", {children: e.text}), " "]}, e.field)))
                })]
            })
        })), gt = (r(223), r(224), function () {
            var e = [];
            this.log = t => e.push({level: "info", message: t}), this.warn = t => e.push({
                level: "warning",
                message: t
            }), this.error = t => e.push({level: "error", message: t}), this.getEntries = () => e.slice(0)
        }), jt = {error: l.i, warning: l.i, info: l.p}, ft = ({entry: e}) => {
            var t = e.level, r = e.message;
            return Object(a.jsxs)("div", {
                className: "LogEntry LogEntry-".concat(t),
                children: [Object(a.jsx)(P.a, {icon: jt[t]}), " ", r]
            })
        },
        xt = Object(S.e)((({entries: e}) => Object(a.jsx)(a.Fragment, {children: e.map(((e, t) => Object(a.jsx)(ft, {entry: e}, t)))}))),
        vt = (r(225), ({
                           label: e, folded: t, onHeaderClick: r = (() => {
            })
                       }) => e ? Object(a.jsx)("h4", {
            className: "SectionDivider",
            children: Object(a.jsxs)("span", {
                onClick: r,
                children: [e, Object(a.jsx)("span", {className: C()("Caret", {CaretRight: t})})]
            })
        }) : null),
        Ot = Object(S.e)((({label: e, children: t, className: r, style: n, folded: i, onHeaderClick: s}) => {
            var o = !!i && i();
            return Object(a.jsxs)("section", {
                className: C()("Section", r),
                style: n,
                children: [Object(a.jsx)(vt, {
                    label: e,
                    folded: o,
                    onHeaderClick: s
                }), Object(a.jsx)("div", {style: X(o), children: t})]
            })
        })), yt = (r(226), Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.description, s = e.options, o = e.inline;
            return Object(a.jsx)(fe.b, {
                className: "RadioSetting",
                label: n,
                description: i,
                children: Object(a.jsx)(D.l, {
                    onChange: t => r(e, t.target.value),
                    selectedValue: t(e),
                    inline: o,
                    children: s.map((e => Object(a.jsx)(D.k, {
                        value: e.value,
                        children: Object(a.jsx)(fe.a, {label: e.label || e.value, description: e.description})
                    }, e.value)))
                })
            })
        }))), wt = (r(227), Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.description;
            return Object(a.jsxs)(D.d, {
                className: "BooleanSetting Setting",
                children: [Object(a.jsx)(D.b, {
                    checked: t(e),
                    label: e.label,
                    inline: !0,
                    onChange: t => r(e, t.target.checked)
                }), n ? Object(a.jsx)(fe.c, {description: n}) : null]
            })
        }))), St = Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.description, s = e.multiLine, o = void 0 !== s && s;
            return Object(a.jsx)(fe.b, {
                className: "StringSetting",
                label: n,
                description: i,
                children: o ? Object(a.jsx)(D.s, {
                    style: {width: "100%", minHeight: "8rem"},
                    value: t(e),
                    onChange: t => r(e, t.target.value)
                }) : Object(a.jsx)(D.f, {value: t(e), onChange: t => r(e, t.target.value)})
            })
        })), Ft = (r(228), [1, 2, 5, 10]), Ct = e => {
            if (0 === e) return Ft[0];
            for (var t = Math.floor(Math.log10(e)), r = e / Math.pow(10, t), a = 0; a < Ft.length; a++) if (r <= Ft[a]) return Ft[a] * Math.pow(10, t)
        }, kt = (e, t = 3) => {
            for (var r = 0; r < t; r++) {
                var a = e * Math.pow(10, r);
                if (Math.floor(a) === a) return r
            }
            return t
        }, Tt = (e, t) => t ? Math.max(1, e) : e, Lt = (e, t, r, a) => {
            var i = e.min, s = e.integer, o = kt(r), c = e => (1 * e).toFixed(Math.min(kt(e), o)),
                l = Object(n.useState)(c(a)), u = Object(h.a)(l, 2), d = u[0], m = u[1];
            Object(n.useEffect)((() => {
                m(a)
            }), [a]);
            return {
                stringValue: d, setStringValue: m, onNumberValueChange: (r, a) => {
                    var n = Math.pow(10, o), l = Math.round(r * n) / n,
                        u = s && Number.isFinite(i) ? Math.max(i, l - l % a) : l;
                    m(c(u)), t(e, u)
                }
            }
        }, It = Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.description, s = e.min, o = e.max, c = e.step, l = e.integer, u = t(e),
                d = Tt(Ct(void 0 !== c ? c : (o - s) / 100), l), h = Lt(e, r, d, u), m = h.stringValue,
                p = h.setStringValue, b = h.onNumberValueChange;
            return Object(a.jsx)(fe.b, {
                className: "NumericSettingSimplte",
                label: n,
                description: i,
                children: Object(a.jsx)(D.d, {
                    inline: !0,
                    fill: !0,
                    className: "NumericSettingControls",
                    children: Object(a.jsx)(D.g, {
                        onBlur: () => b(parseFloat(m), 1),
                        onButtonClick: e => b(e, d),
                        value: m,
                        onValueChange: (e, t) => p(t),
                        fill: !1,
                        min: s,
                        max: o,
                        stepSize: d,
                        minorStepSize: d,
                        majorStepSize: d,
                        clampValueOnBlur: !0
                    })
                })
            })
        })), zt = Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.description, s = e.min, o = e.max, c = e.step, l = e.integer, u = e.onRelease, d = t(e),
                h = o - s, m = void 0 !== c ? c : h / 20, p = Tt(Ct(void 0 !== c ? c : h / 100), l), b = Tt(Ct(m), l),
                g = Math.max(kt(s), kt(o)), j = kt(b), f = () => {
                    u && u()
                }, x = Lt(e, r, p, d), v = x.stringValue, O = x.setStringValue, y = x.onNumberValueChange,
                w = Math.max(Math.min(d, o), s);
            return Object(a.jsx)(fe.b, {
                className: "NumericSetting",
                label: n,
                description: i,
                children: Object(a.jsxs)(D.d, {
                    inline: !0,
                    fill: !0,
                    className: "NumericSettingControls",
                    children: [Object(a.jsx)(D.g, {
                        onBlur: () => {
                            y(parseFloat(v), 1), f()
                        },
                        onButtonClick: e => y(e, p),
                        value: v,
                        onValueChange: (e, t) => O(t),
                        fill: !1,
                        min: s,
                        max: o,
                        stepSize: p,
                        minorStepSize: p,
                        majorStepSize: p,
                        clampValueOnBlur: !0
                    }), Object(a.jsx)(D.m, {
                        value: w,
                        onChange: e => y(e, b),
                        onRelease: f,
                        fill: !1,
                        min: s,
                        max: o,
                        stepSize: b,
                        labelStepSize: h,
                        labelRenderer: e => (1 * e).toFixed(e === s || e === o ? g : j)
                    })]
                })
            })
        })), qt = (r(229), Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.options, s = e.description, o = e.noOptionsMessage,
                c = void 0 === o ? "No options to choose from." : o, l = "function" === typeof i ? i() : i,
                u = l && l.length > 0 ? Object(a.jsx)(D.e, {
                    onChange: t => r(e, t.target.value),
                    value: t(e),
                    fill: !0,
                    children: l.map((e => Object(a.jsx)("option", {
                        value: e.value,
                        title: e.description,
                        children: e.label || e.value
                    }, e.value)))
                }) : Object(a.jsx)("small", {children: c});
            return Object(a.jsx)(fe.b, {className: "SelectSetting", label: n, description: s, children: u})
        }))), Nt = Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.description;
            return Object(a.jsx)(fe.b, {
                className: "StringListSetting",
                label: n,
                description: i,
                children: Object(a.jsx)(D.r, {
                    values: t(e),
                    onChange: t => r(e, t),
                    fill: !0,
                    tagProps: {minimal: !0, intent: "primary"},
                    addOnBlur: !0
                })
            })
        })), Rt = (r(230), r(114)), Dt = r.n(Rt), Pt = r(116), Mt = Object(S.e)((({setting: e, get: t, set: r}) => {
            var i = e.label, s = e.description, o = Object(S.d)({file: null}), c = Object(n.useCallback)((t => {
                    if (t.length > 0) {
                        var a = t[0];
                        o.file = a, r(e, a)
                    }
                }), [r, e, o]), l = Object(Pt.a)({onDrop: c, multiple: !1}), u = l.getRootProps, d = l.getInputProps,
                h = l.isDragActive, m = o.file ? Object(a.jsxs)("div", {
                    className: "FileSettingFileInfo",
                    children: [Object(a.jsx)("span", {children: o.file.name}), Object(a.jsx)("span", {children: Dt()(o.file.size)}), Object(a.jsx)("span", {children: o.file.type})]
                }) : null;
            return Object(a.jsx)(fe.b, {
                className: "FileSetting",
                label: i,
                description: s,
                children: Object(a.jsxs)("div", Object(T.a)(Object(T.a)({}, u()), {}, {
                    children: [Object(a.jsx)("input", Object(T.a)({}, d())), Object(a.jsxs)("div", {
                        className: C()("FileSettingDropZone", {FileSettingDropZoneActive: h}),
                        children: [m, Object(a.jsxs)("div", {
                            children: [Object(a.jsx)(D.a, {
                                small: !0,
                                children: "Browse"
                            }), " or drag 'n' drop your file here."]
                        })]
                    })]
                }))
            })
        })), Et = (r(231), Object(S.e)((({store: e, onClick: t}) => {
            var r = "ok" === e.status;
            return Object(a.jsx)(D.a, {
                className: C()({ExtraPadding: !r}),
                icon: Object(a.jsx)(P.a, {icon: r ? l.c : l.s}),
                intent: r ? "success" : "none",
                title: r ? "Connected" : "Connect to Solr",
                text: r ? "" : "Connect",
                loading: "loading" === e.status,
                onClick: t,
                outlined: r
            })
        }))), At = Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.description, s = e.stateStore, o = e.checkUrl, c = Object(S.d)({
                url: t(e), setUrl: e => {
                    c.url = e, s.urlDirty()
                }
            }), l = s.message ? Object(a.jsx)(ft, {entry: {level: "error", message: s.message}}) : null;
            return Object(a.jsx)(fe.b, {
                className: "ServiceUrlSetting",
                label: n,
                description: i,
                message: l,
                children: Object(a.jsxs)(D.c, {
                    fill: !0,
                    children: [Object(a.jsx)(D.f, {
                        value: c.url,
                        fill: !0,
                        onChange: e => c.setUrl(e.target.value)
                    }), Object(a.jsx)(Et, {store: s, onClick: () => o(c.url)})]
                })
            })
        })), Bt = (r(232), () => Object(a.jsx)("div", {className: "Deferred", children: "Initializing..."})),
        Wt = Object(S.e)((e => {
            var t = e.timeout, r = e.setting, i = Object(_.a)(e, ["timeout", "setting"]), s = ((e, t) => {
                var r = Object(T.a)({}, e), a = r.settings, i = Object(_.a)(r, ["settings"]),
                    s = Object(n.useState)(!0), o = Object(h.a)(s, 2), c = o[0], l = o[1];
                Object(n.useEffect)((() => {
                    var e = setTimeout((() => {
                        l(!1)
                    }), t);
                    return () => {
                        clearTimeout(e)
                    }
                }), [l, t]);
                var u = a.filter(fe.d);
                return i.settings = c ? u.slice(0, 1) : a, [i, c && u.length > 1]
            })(r, t), o = Object(h.a)(s, 2), c = o[0], l = o[1] ? Object(a.jsx)(Bt, {}) : null;
            return Object(a.jsxs)(a.Fragment, {children: [Object(a.jsx)(Jt, Object(T.a)({setting: c}, i)), l]})
        })), Jt = Object(S.e)((({setting: e, get: t, set: r, className: n}) => {
            var i = e.label, s = e.description, o = !1, c = e.settings.map((n => {
                var i = Object(fe.d)(n);
                return o |= i, Object(a.jsx)("section", {
                    id: n.id,
                    style: X(!i),
                    children: (n.factory || Vt(n))(n, n.get || e.get || t, n.set || e.set || r)
                }, n.id)
            }));
            return i ? Object(a.jsxs)(Ot, {
                className: n,
                label: i,
                style: X(!o),
                folded: e.folded,
                onHeaderClick: e.onHeaderClick,
                children: [Object(a.jsx)("p", {children: s}), c]
            }) : Object(a.jsx)("section", {className: n, style: X(!o), children: c})
        })), Ht = {
            group: (e, t, r) => Object(a.jsx)(Jt, {setting: e, get: t, set: r}),
            boolean: (e, t, r) => Object(a.jsx)(wt, {setting: e, get: t, set: r}),
            string: (e, t, r) => Object(a.jsx)(St, {setting: e, get: t, set: r}),
            file: (e, t, r) => Object(a.jsx)(Mt, {setting: e, get: t, set: r}),
            "string-array": (e, t, r) => Object(a.jsx)(Nt, {setting: e, get: t, set: r}),
            enum: (e, t, r) => "radio" === e.ui ? Object(a.jsx)(yt, {
                setting: e,
                get: t,
                set: r
            }) : "select" === e.ui ? Object(a.jsx)(qt, {setting: e, get: t, set: r}) : void 0,
            number: (e, t, r) => Number.isFinite(e.min) && Number.isFinite(e.max) ? Object(a.jsx)(zt, {
                setting: e,
                get: t,
                set: r
            }) : Object(a.jsx)(It, {setting: e, get: t, set: r}),
            "service-url": (e, t, r) => Object(a.jsx)(At, {setting: e, get: t, set: r})
        }, Vt = e => {
            var t = Ht[e.type];
            if (!t) throw new Error("Unknown factory for setting type: ".concat(e.type));
            return t
        }, Ut = r(27), Qt = r(69), _t = e => {
            if (!e.charAt) return 0;
            for (var t = 0, r = 0; r < e.length; r++) " " === e.charAt(r) && t++;
            return t
        }, Gt = e => {
            var t = (e => Array.from(e.reduce(((e, t) => (Object(st.b)(t, ((t, r) => {
                e.add(r)
            })), e)), new Set)))(e), r = ((e, t) => {
                var r = t.reduce(((e, t) => (e.set(t, new Map), e)), new Map);
                return e.forEach((e => {
                    Object(st.b)(e, ((e, t) => {
                        var a = Array.isArray(e) ? null === e || void 0 === e ? void 0 : e[0] : e;
                        Object(st.c)(r.get(t), Object.prototype.toString.call(a), 1)
                    }))
                })), Array.from(r.keys()).reduce(((e, t) => {
                    var a = 0, n = null;
                    return r.get(t).forEach(((e, t) => {
                        a < e && (a = e, n = t)
                    })), e.set(t, n.substring(0, n.length - 1).substring(8)), e
                }), new Map)
            })(e, t), a = ((e, t) => {
                var r = t.reduce(((e, t) => (e.set(t, {
                    length: new Qt.Stats,
                    count: new Qt.Stats,
                    empty: 0,
                    distinct: 0,
                    spaces: new Qt.Stats
                }), e)), new Map);
                return t.forEach((t => {
                    var a = new Set;
                    e.forEach((e => {
                        var n = e[t], i = r.get(t);
                        null !== n && void 0 !== n ? Array.isArray(n) ? (i.count.push(n.length), n.forEach((e => {
                            i.length.push(e.length || (e + "").length), i.spaces.push(_t(e)), a.add(e)
                        }))) : (i.count.push(1), i.length.push(n.length || (n + "").length), i.spaces.push(_t(n)), a.add(n)) : i.empty++
                    })), r.get(t).distinct = a.size
                })), t.reduce(((e, t) => {
                    var a = r.get(t);
                    return e.set(t, {
                        empty: a.empty,
                        distinct: a.distinct,
                        length: {avg: a.length.amean(), dev: a.length.\u03c3()},
                        count: {avg: a.count.amean(), dev: a.count.\u03c3()},
                        spaces: {avg: a.spaces.amean(), dev: a.spaces.\u03c3()}
                    }), e
                }), new Map)
            })(e, t), n = t.map((e => Object.assign({field: e, type: r.get(e)}, a.get(e))));
            return ((e, t) => {
                e.forEach((e => {
                    var r = Math.pow(2, 16 / e.length.avg), a = (e.count.avg - 1) * e.distinct / (t * (e.spaces.avg + 1)),
                        n = Math.pow(2, 16 / e.distinct) / (e.spaces.avg + 1), i = e.length.avg >= 4 ? 1 : 0,
                        s = e.spaces.avg;
                    "String" !== e.type && (i = 0, s = 0), /title/i.test(e.field) && (i *= 4, s *= 2), /content|body|abstract|comment|question|answer|post|message/i.test(e.field) && (i *= 2, s *= 2), e.distinct === t && 1 === e.count.avg && (i *= 2, r *= 2);
                    var o = e.distinct / (e.count.avg * t);
                    s *= 1 === o ? 2 : 1 / Math.exp(Math.abs(2 * (o - 1))), e.distinct !== t && (r = 0), e.length.avg > 10 && e.length.avg < 200 && (i *= 2), e.length.avg <= 16 && (s = 0), e.titleScore = i, e.naturalTextScore = s, e.idScore = r, e.tagScore = a, e.propScore = n
                }))
            })(n, e.length), n
        }, Kt = (e, t) => {
            var r = Gt(e), a = r.map((e => e.field)),
                n = r.filter((e => e.naturalTextScore >= 8 || e.titleScore >= 8)).map((e => e.field)), i = /^https?:\/\//i,
                s = r.filter((e => "String" === e.type));
            return e.forEach((e => {
                if (void 0 === e.url) {
                    var t, r = Object(Ut.a)(s);
                    try {
                        for (r.s(); !(t = r.n()).done;) {
                            var a = t.value, n = e[a.field];
                            if (a.naturalTextScore < 2 && i.test(n)) {
                                e.url = n;
                                break
                            }
                        }
                    } catch (o) {
                        r.e(o)
                    } finally {
                        r.f()
                    }
                }
            })), {fieldStats: r, fieldsAvailable: a, fieldsAvailableForClustering: n, fieldsToCluster: n}
        }, Xt = e => {
            var t = {query: "", documents: []}, r = Object(S.d)({
                loading: !1,
                log: [],
                fileLoaded: !1,
                fieldStats: [],
                fieldsAvailable: [],
                fieldsAvailableForClustering: [],
                clusterNaturalTextOnly: !0,
                getFieldsAvailableForClustering: e => {
                    var t = r.fieldStats;
                    return Array.from((e ? t.filter((e => e.naturalTextScore >= 8 || e.titleScore >= 8)) : t.filter((e => "String" === e.type))).map((e => e.field))).sort()
                },
                fieldsToCluster: [],
                load: function () {
                    var e = Object(rt.a)(tt.a.mark((function e(i) {
                        var s, o, c, l, u, d;
                        return tt.a.wrap((function (e) {
                            for (; ;) switch (e.prev = e.next) {
                                case 0:
                                    return r.loading = !0, s = new gt, e.prev = 2, e.next = 5, i(s);
                                case 5:
                                    o = e.sent, c = Kt(o.documents), (l = n.get(a(c.fieldsAvailable))) && l.length > 0 ? (d = new Set(l), u = new Set([...c.fieldsToCluster].filter((e => d.has(e))))) : u = new Set(c.fieldsToCluster), r.fieldsToCluster = u, r.fieldStats = c.fieldStats, r.fieldsAvailable = c.fieldsAvailable, r.fileLoaded = !0, t.documents = o.documents, t.query = o.query, e.next = 20;
                                    break;
                                case 17:
                                    e.prev = 17, e.t0 = e.catch(2), s.error(e.t0 instanceof Error ? e.t0.toString() : e.t0);
                                case 20:
                                    return e.prev = 20, r.log = s.getEntries(), r.loading = !1, e.finish(20);
                                case 24:
                                case"end":
                                    return e.stop()
                            }
                        }), e, null, [[2, 17, 20, 24]])
                    })));
                    return function (t) {
                        return e.apply(this, arguments)
                    }
                }()
            }), a = e => e.join("--"), n = Object(z.a)("workbench:source:".concat(e, ":lastConfigs"), (() => {
                var e = r.fieldsAvailable;
                return e.length > 0 ? a(e) : null
            }), (() => Array.from(r.fieldsToCluster)));
            return {schemaInfoStore: r, resultHolder: t}
        }, Yt = Object(S.e)((({schemaInfoStore: e}) => {
            var t = e, r = t.getFieldsAvailableForClustering(t.clusterNaturalTextOnly), n = t.fieldsToCluster,
                i = 0 === r.length ? Object(a.jsx)("small", {children: "No natural text content detected"}) : null;
            return Object(a.jsxs)("div", {
                className: "FieldList",
                children: [i, r.map((e => Object(a.jsx)(D.b, {
                    label: e, checked: n.has(e), onChange: t => {
                        t.target.checked ? n.add(e) : n.delete(e)
                    }
                }, e)))]
            })
        })), Zt = Object(S.e)((({schemaInfoStore: e}) => {
            var t = e, r = t.clusterNaturalTextOnly;
            return Object(a.jsx)("div", {
                className: "FieldChoiceFieldFilter",
                children: r ? Object(a.jsxs)(a.Fragment, {
                    children: ["Only natural text fields shown,", " ", Object(a.jsx)(G.a, {
                        onClick: () => t.clusterNaturalTextOnly = !1,
                        children: "show all fields"
                    }), "."]
                }) : Object(a.jsxs)(a.Fragment, {
                    children: ["All string-typed fields shown,", " ", Object(a.jsx)(G.a, {
                        onClick: () => t.clusterNaturalTextOnly = !0,
                        children: "show text fields"
                    }), "."]
                })
            })
        })), $t = Object(S.e)((({setting: e, get: t, set: r}) => {
            var n = e.label, i = e.description, s = e.schemaInfoStore;
            return Object(a.jsxs)(fe.b, {
                className: "FieldChoiceSetting",
                label: n,
                description: i,
                children: [Object(a.jsx)(k, {isLoading: () => s.loading}), Object(a.jsx)(Yt, {schemaInfoStore: s}), Object(a.jsx)(xt, {entries: s.log}), Object(a.jsx)(Zt, {schemaInfoStore: s})]
            })
        }));
    Ue = (e, t, r) => Object(a.jsx)($t, {setting: e, get: t, set: r}), Ht["field-choice"] = Ue;
    var er = (e, t, r) => Object.assign({
            id: "".concat(e, ":fieldChoice"),
            type: "field-choice",
            label: "Fields to cluster",
            visible: () => t.loading || t.fileLoaded || t.log.length > 0,
            get: () => t.fieldsToCluster,
            set: () => {
            },
            schemaInfoStore: t
        }, r), tr = (e, t, r) => {
            var n;
            return Object(S.a)((() => {
                n = Array.from(e.fieldsToCluster)
            })), Object.assign(r, {
                createResult: e => Object(a.jsx)(bt, Object(T.a)(Object(T.a)({}, e), {}, {configStore: t})),
                createConfig: () => Object(a.jsx)(pt, {configStore: t}),
                createSourceConfig: () => {
                    throw new Error("Not available in search app.")
                },
                getFieldsToCluster: () => n
            })
        }, rr = function () {
            var e = Object(rt.a)(tt.a.mark((function e(t, a) {
                var n, i, s, o, c, l, u, d, h, m, p, b, g, j, f;
                return tt.a.wrap((function (e) {
                    for (; ;) switch (e.prev = e.next) {
                        case 0:
                            return e.next = 2, Promise.all([r.e(1), r.e(0)]).then(r.t.bind(null, 274, 7));
                        case 2:
                            return n = e.sent, e.next = 5, t.arrayBuffer();
                        case 5:
                            if (i = e.sent, s = n.read(i, {type: "array"}), o = s.Sheets[s.SheetNames[0]], c = "The spreadsheet contains no data.", l = o["!ref"]) {
                                e.next = 13;
                                break
                            }
                            return a.info(c), e.abrupt("return", ar);
                        case 13:
                            if (!((u = n.utils.decode_range(l)).e.r <= 0)) {
                                e.next = 17;
                                break
                            }
                            return a.info(c), e.abrupt("return", ar);
                        case 17:
                            for (d = (e, t) => o[n.utils.encode_cell({c: t, r: e})], h = (e, t) => {
                                var r = d(e, t);
                                return r && r.v
                            }, m = [], p = 0; p <= u.e.c; p++) m.push(h(0, p));
                            for (b = [], g = 1; g < u.e.r; g++) {
                                for (j = {}, f = 0; f <= u.e.c; f++) j[m[f]] = h(g, f);
                                b.push(j)
                            }
                            return e.abrupt("return", nr(b));
                        case 24:
                        case"end":
                            return e.stop()
                    }
                }), e)
            })));
            return function (t, r) {
                return e.apply(this, arguments)
            }
        }(), ar = {documents: [], query: ""}, nr = (e, t = "") => ({documents: e, query: t}), ir = {
            "text/xml": function () {
                var e = Object(rt.a)(tt.a.mark((function e(t, a) {
                    var n, i, s;
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2, t.text();
                            case 2:
                                return n = e.sent, e.next = 5, r.e(10).then(r.t.bind(null, 275, 7));
                            case 5:
                                if (i = e.sent, (s = i.parse(n)).searchresult) {
                                    e.next = 12;
                                    break
                                }
                                return a.error("XML must be in Carrot2 format."), e.abrupt("return", ar);
                            case 12:
                                return e.abrupt("return", nr(s.searchresult.document, s.searchresult.query));
                            case 13:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                })));
                return function (t, r) {
                    return e.apply(this, arguments)
                }
            }(),
            "application/json": function () {
                var e = Object(rt.a)(tt.a.mark((function e(t) {
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.t0 = nr, e.t1 = JSON, e.next = 4, t.text();
                            case 4:
                                return e.t2 = e.sent, e.t3 = e.t1.parse.call(e.t1, e.t2), e.abrupt("return", (0, e.t0)(e.t3));
                            case 7:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                })));
                return function (t) {
                    return e.apply(this, arguments)
                }
            }(),
            "application/vnd.oasis.opendocument.spreadsheet": rr,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": rr,
            "application/vnd.ms-excel": rr
        }, sr = function () {
            var e = Object(rt.a)(tt.a.mark((function e(t, r) {
                var a, n;
                return tt.a.wrap((function (e) {
                    for (; ;) switch (e.prev = e.next) {
                        case 0:
                            if (a = ir[t.type]) {
                                e.next = 4;
                                break
                            }
                            return r.error("Unknown file type ".concat(t.type, ".")), e.abrupt("return", ar);
                        case 4:
                            return e.next = 6, a(t, r);
                        case 6:
                            return n = e.sent, r.log("".concat(Object(Y.c)(n.documents.length, "document", !0), " loaded.")), e.abrupt("return", n);
                        case 9:
                        case"end":
                            return e.stop()
                    }
                }), e)
            })));
            return function (t, r) {
                return e.apply(this, arguments)
            }
        }(), or = ct("localFile"), cr = Xt("localFile"), lr = cr.schemaInfoStore, ur = cr.resultHolder, dr = () => {
            var e = "[\n" + mr.map((e => "  " + JSON.stringify(e))).join(",\n") + ",\n  ...\n]";
            return Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)("p", {children: "The following file types are supported:"}), Object(a.jsxs)("ul", {
                    children: [Object(a.jsx)("li", {children: Object(a.jsxs)("p", {children: [Object(a.jsx)("strong", {children: "Excel, OpenOffice, CSV"}), " (", Object(a.jsx)(pr, {file: "serverfault.xlsx"}), ") \u2014 one document per row, the first row is treated as a header with document field names."]})}), Object(a.jsxs)("li", {children: [Object(a.jsxs)("p", {children: [Object(a.jsx)("strong", {children: "JSON"}), " (", Object(a.jsx)(pr, {file: "serverfault.json"}), ") \u2014 an array of flat JSON objects representing documents to cluster:"]}), Object(a.jsx)(it, {jsonString: e}), Object(a.jsxs)("p", {children: ["The objects can have text and non-text fields, Carrot", Object(a.jsx)("sup", {children: "2"}), " ", "will try to detect the ones to cluster."]})]}), Object(a.jsx)("li", {
                        children: Object(a.jsxs)("p", {
                            children: [Object(a.jsx)("strong", {children: "XML"}), " (", Object(a.jsx)(pr, {file: "seattle.xml"}), ") \u2013 the", " ", Object(a.jsxs)("a", {
                                href: "https://doc.carrot2.org/#section.architecture.input-xml",
                                target: "_blank",
                                rel: "noreferrer",
                                children: ["legacy Carrot", Object(a.jsx)("sup", {children: "2"}), " XML format"]
                            }), "."]
                        })
                    })]
                })]
            })
        }, hr = [{
            id: "file",
            type: "group",
            label: "Local file",
            description: "Loads documents from a local file. Carrot2 XML, JSON, CSV and Excel formats are supported.",
            settings: [{
                id: "file:file",
                type: "file",
                label: "File",
                description: Object(a.jsxs)(a.Fragment, {children: [Object(a.jsx)("p", {children: "The file from which to read data for clustering."}), Object(a.jsx)(dr, {})]}),
                get: () => null,
                set: (e, t) => {
                    lr.load(function () {
                        var e = Object(rt.a)(tt.a.mark((function e(r) {
                            return tt.a.wrap((function (e) {
                                for (; ;) switch (e.prev = e.next) {
                                    case 0:
                                        return e.abrupt("return", sr(t, r));
                                    case 1:
                                    case"end":
                                        return e.stop()
                                }
                            }), e)
                        })));
                        return function (t) {
                            return e.apply(this, arguments)
                        }
                    }())
                }
            }, er("file", lr)]
        }], mr = [{title: "Title 1", body: "Text", views: 583}, {title: "Title 2", body: "Text", views: 23}],
        pr = ({file: e}) => Object(a.jsx)("a", {
            href: "workbench/examples/".concat(e),
            download: !0,
            children: "download sample"
        }), br = tr(lr, or, {
            label: "Local file",
            descriptionHtml: "content read from a local file in Carrot2 XML, JSON, CSV or Excel format.",
            contentSummary: "Excel, CSV, OpenOffice, JSON or XML files",
            source: () => (or.load(lr.fieldStats, ur), {
                query: ur.query,
                matches: ur.documents.length,
                documents: ur.documents
            }),
            getSettings: () => hr,
            createError: e => Object(a.jsx)(we.a, {error: e}),
            createIntroHelp: () => Object(a.jsxs)(a.Fragment, {children: [Object(a.jsx)("p", {children: "Data for clustering is extracted from the file you provide."}), Object(a.jsx)(dr, {})]})
        }), gr = r(57), jr = Object(z.b)("workbench:source", {source: "web"}), fr = ({
                                                                                         id: e,
                                                                                         serviceName: t,
                                                                                         configOverrides: r,
                                                                                         querySetting: a,
                                                                                         fetchCollections: n,
                                                                                         fetchResultsForSchemaInference: i
                                                                                     }) => {
            var s = Xt(e), o = s.schemaInfoStore, c = s.resultHolder, l = ct(e),
                u = Object(z.b)("workbench:source:".concat(e, ":serviceConfig"), Object.assign({
                    collection: void 0,
                    maxResults: 100
                }, r)), d = (e => {
                    var t = Object(S.d)(Object.assign({
                        message: null, status: "pending", urlDirty: () => {
                            t.status = "pending"
                        }
                    }, e));
                    return t
                })({
                    isUrlValid: () => "ok" === d.status, checkServiceUrl: function () {
                        var e = Object(rt.a)(tt.a.mark((function e(t) {
                            var r;
                            return tt.a.wrap((function (e) {
                                for (; ;) switch (e.prev = e.next) {
                                    case 0:
                                        return d.status = "loading", d.message = "", e.prev = 2, e.next = 5, n(t);
                                    case 5:
                                        r = e.sent, u.serviceUrl = t, d.status = "ok", d.collections = r, r.indexOf(u.collection) < 0 && (u.collection = r[0]), e.next = 16;
                                        break;
                                    case 12:
                                        e.prev = 12, e.t0 = e.catch(2), d.status = "error", d.message = e.t0 instanceof Error ? e.t0.toString() : e.t0;
                                    case 16:
                                    case"end":
                                        return e.stop()
                                }
                            }), e, null, [[2, 12]])
                        })));
                        return function (t) {
                            return e.apply(this, arguments)
                        }
                    }(), collections: []
                }), h = () => d.isUrlValid() && !!u.collection;
            Object(S.a)((() => {
                jr.source === e && d.checkServiceUrl(u.serviceUrl)
            })), Object(S.a)((() => {
                jr.source === e && h() && o.load(Object(rt.a)(tt.a.mark((function e() {
                    var t;
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2, i();
                            case 2:
                                return t = e.sent, c.documents = t.documents, e.abrupt("return", t);
                            case 5:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                }))))
            }));
            var m = [{
                id: "".concat(e, ":serviceUrl"),
                type: "service-url",
                label: "".concat(t, " service URL"),
                urlStore: d,
                get: () => u.serviceUrl,
                stateStore: d,
                checkUrl: d.checkServiceUrl
            }, {
                id: "".concat(e, ":collection"),
                type: "enum",
                ui: "select",
                label: "".concat(t, " collection to search"),
                noOptionsMessage: "Collection list is empty, no content to search.",
                options: () => d.collections.map((e => ({value: e}))),
                visible: () => d.isUrlValid(),
                get: () => u.collection,
                set: (e, t) => u.collection = t
            }, er(e, o, {visible: () => h()}), a(e), Object(T.a)({
                id: "".concat(e, ":maxResults"),
                type: "number",
                label: "Max results",
                min: 0,
                max: 1e4,
                step: 100,
                description: "<p>The number of search results to fetch.</p>",
                visible: () => h()
            }, Object(fe.e)(u, "maxResults"))];
            return {
                serviceConfigStore: u,
                serviceStateStore: d,
                isSearchPossible: h,
                settings: m,
                afterSuccessfulSearch: () => {
                    l.load(o.fieldStats, c)
                },
                createLocalSearchSource: e => tr(o, l, e)
            }
        }, xr = fr({
            id: "solr",
            serviceName: "Solr",
            configOverrides: {serviceUrl: "http://localhost:8983/solr", extraHttpGetParams: ""},
            querySetting: e => Object(T.a)(Object(T.a)({id: "".concat(e, ":query")}, Object(fe.e)(ye, "query")), {}, {
                type: "string",
                label: "Query",
                description: '\n<p>\n  The search query to pass to Solr. Use \n  <a target=_blank href="https://lucene.apache.org/solr/guide/8_6/the-standard-query-parser.html#specifying-terms-for-the-standard-query-parser">Solr query syntax</a>.\n</p>',
                visible: () => Or()
            }),
            fetchCollections: function () {
                var e = Object(rt.a)(tt.a.mark((function e(t) {
                    var r;
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2, gr.a.get("admin/cores?action=STATUS", {
                                    prefixUrl: t,
                                    timeout: 4e3
                                }).json();
                            case 2:
                                return r = e.sent, e.abrupt("return", Object.keys(r.status));
                            case 4:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                })));
                return function (t) {
                    return e.apply(this, arguments)
                }
            }(),
            fetchResultsForSchemaInference: function () {
                var e = Object(rt.a)(tt.a.mark((function e() {
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.abrupt("return", Fr("*:*", 50));
                            case 1:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                })));
                return function () {
                    return e.apply(this, arguments)
                }
            }()
        }), vr = xr.serviceConfigStore, Or = xr.isSearchPossible, yr = xr.settings, wr = xr.afterSuccessfulSearch,
        Sr = xr.createLocalSearchSource, Fr = function () {
            var e = Object(rt.a)(tt.a.mark((function e(t, r = 50, a) {
                var n, i, s;
                return tt.a.wrap((function (e) {
                    for (; ;) switch (e.prev = e.next) {
                        case 0:
                            if (n = vr.serviceUrl, i = vr.collection) {
                                e.next = 4;
                                break
                            }
                            return e.abrupt("return", {documents: [], matches: 0, query: ""});
                        case 4:
                            return e.next = 6, gr.a.get("".concat(i, "/select"), {
                                prefixUrl: n,
                                timeout: 4e3,
                                searchParams: Object.assign({}, a, {q: t, rows: r})
                            }).json();
                        case 6:
                            return s = e.sent, e.abrupt("return", {
                                documents: s.response.docs,
                                matches: s.response.numFound,
                                query: t
                            });
                        case 8:
                        case"end":
                            return e.stop()
                    }
                }), e)
            })));
            return function (t) {
                return e.apply(this, arguments)
            }
        }(), Cr = [{
            id: "solr",
            type: "group",
            label: "Solr",
            description: "Queries Apache Solr.",
            settings: [...yr, Object(T.a)({
                id: "solr:extraParameters",
                type: "string",
                advanced: !0,
                label: "Additional search request parameters",
                description: "\n<p>\n  The extra HTTP GET parameters to pass to the <code>/select</code> endpoint, for example: \n</p>\n<pre>defType=dismax&fq=category:important</pre>",
                visible: () => Or()
            }, Object(fe.e)(vr, "extraHttpGetParams"))]
        }], kr = () => Object(a.jsxs)(a.Fragment, {
            children: [Object(a.jsxs)("p", {children: ["Provide the address of your Solr instance in the", " ", Object(a.jsx)("strong", {children: "Solr service URL"}), " field and press", " ", Object(a.jsx)("strong", {children: "Connect"}), ". Make sure the instance emits correct CORS headers, otherwise the connection will fail."]}), Object(a.jsxs)("p", {
                children: ["Once Workbench connects to your Solr instance, it will fetch the list of available Solr cores. Choose the core you'd like to query and type your query using", " ", Object(a.jsx)("a", {
                    target: "_blank",
                    rel: "noreferrer",
                    href: "https://lucene.apache.org/solr/guide/8_6/the-standard-query-parser.html#specifying-terms-for-the-standard-query-parser",
                    children: "Solr query syntax"
                }), "."]
            })]
        }), Tr = Sr({
            label: "Solr",
            descriptionHtml: "queries an Apache Solr instance.",
            contentSummary: "Apache Solr search results",
            source: function () {
                var e = Object(rt.a)(tt.a.mark((function e(t) {
                    var r;
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return r = {}, new URLSearchParams(vr.extraHttpGetParams).forEach(((e, t) => {
                                    r[t] = e
                                })), e.abrupt("return", Fr(t, vr.maxResults, r).then((e => (wr(), e))));
                            case 3:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                })));
                return function (t) {
                    return e.apply(this, arguments)
                }
            }(),
            getSettings: () => Cr,
            createError: function () {
                var e = Object(rt.a)(tt.a.mark((function e(t) {
                    var r, n;
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                if (!t.response) {
                                    e.next = 14;
                                    break
                                }
                                return e.prev = 1, e.next = 4, t.response.json();
                            case 4:
                                n = e.sent, r = Object(a.jsx)("pre", {children: n.error.msg}), e.next = 14;
                                break;
                            case 8:
                                return e.prev = 8, e.t0 = e.catch(1), e.next = 12, t.response.text();
                            case 12:
                                n = e.sent, r = Object(a.jsx)("pre", {children: n});
                            case 14:
                                return e.abrupt("return", Object(a.jsx)(we.c, {
                                    children: Object(a.jsx)(we.b, {
                                        error: t,
                                        children: r
                                    })
                                }));
                            case 15:
                            case"end":
                                return e.stop()
                        }
                    }), e, null, [[1, 8]])
                })));
                return function (t) {
                    return e.apply(this, arguments)
                }
            }(),
            createIntroHelp: () => Object(a.jsx)(kr, {})
        }), Lr = fr({
            id: "es",
            serviceName: "Elasticsearch",
            configOverrides: {serviceUrl: "http://localhost:9200/", extraHttpGetParams: ""},
            querySetting: e => Object(T.a)(Object(T.a)({id: "".concat(e, ":query")}, Object(fe.e)(ye, "query")), {}, {
                type: "string",
                label: "Query",
                description: '\n<p>\n  The search query to pass to Elasticsearch. Use \n  <a target=_blank href="https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax">Elasticsearch DSL query syntax</a>.\n</p>',
                visible: () => Rr()
            }),
            fetchCollections: function () {
                var e = Object(rt.a)(tt.a.mark((function e(t) {
                    var r;
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.next = 2, gr.a.get("_cat/indices?format=json", {
                                    prefixUrl: t,
                                    timeout: 4e3
                                }).json();
                            case 2:
                                return r = e.sent, e.abrupt("return", r.map((e => e.index)));
                            case 4:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                })));
                return function (t) {
                    return e.apply(this, arguments)
                }
            }(),
            fetchResultsForSchemaInference: function () {
                var e = Object(rt.a)(tt.a.mark((function e() {
                    return tt.a.wrap((function (e) {
                        for (; ;) switch (e.prev = e.next) {
                            case 0:
                                return e.abrupt("return", Dr("*:*", 50));
                            case 1:
                            case"end":
                                return e.stop()
                        }
                    }), e)
                })));
                return function () {
                    return e.apply(this, arguments)
                }
            }()
        }), Ir = Lr.serviceConfigStore, zr = Lr.settings, qr = Lr.afterSuccessfulSearch, Nr = Lr.createLocalSearchSource,
        Rr = Lr.isSearchPossible, Dr = function () {
            var e = Object(rt.a)(tt.a.mark((function e(t, r = 50) {
                var a, n, i;
                return tt.a.wrap((function (e) {
                    for (; ;) switch (e.prev = e.next) {
                        case 0:
                            if (a = Ir.serviceUrl, n = Ir.collection) {
                                e.next = 4;
                                break
                            }
                            return e.abrupt("return", {documents: [], matches: 0, query: ""});
                        case 4:
                            return e.next = 6, gr.a.get("".concat(n, "/_search"), {
                                prefixUrl: a,
                                timeout: 4e3,
                                searchParams: {
                                    source: JSON.stringify({
                                        query: {query_string: {query: t}},
                                        from: 0,
                                        size: r
                                    }), source_content_type: "application/json"
                                }
                            }).json();
                        case 6:
                            return i = e.sent, e.abrupt("return", {
                                documents: i.hits.hits.map((e => e._source)),
                                matches: i.hits.total,
                                query: t
                            });
                        case 8:
                        case"end":
                            return e.stop()
                    }
                }), e)
            })));
            return function (t) {
                return e.apply(this, arguments)
            }
        }(), Pr = [{
            id: "es",
            type: "group",
            label: "Elasticsearch",
            description: "Queries Elasticsearch.",
            settings: [...zr]
        }], Mr = () => Object(a.jsxs)(a.Fragment, {
            children: [Object(a.jsxs)("p", {children: ["Provide the address of your Elasticsearch instance in the", " ", Object(a.jsx)("strong", {children: "Elasticsearch service URL"}), " field and press", " ", Object(a.jsx)("strong", {children: "Connect"}), "."]}), Object(a.jsxs)("p", {
                children: ["Make sure Elasticsearch is configured with", " ", Object(a.jsx)("a", {
                    href: "https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-http.html",
                    target: "_blank",
                    rel: "noreferrer",
                    children: "CORS headers"
                }), " ", "enabled, otherwise the connection will fail."]
            }), Object(a.jsxs)("p", {
                children: ["Once Workbench connects to your Elasticsearch instance, it will fetch the list of available indices. Choose the index you'd like to query and type your query using", " ", Object(a.jsx)("a", {
                    target: "_blank",
                    rel: "noreferrer",
                    href: "https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax",
                    children: "Elasticsearch DSL query syntax"
                }), "."]
            })]
        }), Er = {
            web: Be, pubmed: $e, file: br, solr: Tr, es: Nr({
                label: "Elasticsearch",
                descriptionHtml: "queries an Elasticsearch instance.",
                contentSummary: "Elasticsearch results",
                source: function () {
                    var e = Object(rt.a)(tt.a.mark((function e(t) {
                        return tt.a.wrap((function (e) {
                            for (; ;) switch (e.prev = e.next) {
                                case 0:
                                    return e.abrupt("return", Dr(t, Ir.maxResults).then((e => (qr(), e))));
                                case 1:
                                case"end":
                                    return e.stop()
                            }
                        }), e)
                    })));
                    return function (t) {
                        return e.apply(this, arguments)
                    }
                }(),
                getSettings: () => Pr,
                createError: function () {
                    var e = Object(rt.a)(tt.a.mark((function e(t) {
                        var r, n;
                        return tt.a.wrap((function (e) {
                            for (; ;) switch (e.prev = e.next) {
                                case 0:
                                    if (!t.response) {
                                        e.next = 14;
                                        break
                                    }
                                    return e.prev = 1, e.next = 4, t.response.json();
                                case 4:
                                    n = e.sent, r = Object(a.jsx)("pre", {children: JSON.stringify(n, null, "  ")}), e.next = 14;
                                    break;
                                case 8:
                                    return e.prev = 8, e.t0 = e.catch(1), e.next = 12, t.response.text();
                                case 12:
                                    n = e.sent, r = Object(a.jsx)("pre", {children: n});
                                case 14:
                                    return e.abrupt("return", Object(a.jsx)(we.c, {
                                        children: Object(a.jsx)(we.b, {
                                            error: t,
                                            children: r
                                        })
                                    }));
                                case 15:
                                case"end":
                                    return e.stop()
                            }
                        }), e, null, [[1, 8]])
                    })));
                    return function (t) {
                        return e.apply(this, arguments)
                    }
                }(),
                createIntroHelp: () => Object(a.jsx)(Mr, {})
            })
        }, Ar = {web: Er.web, pubmed: Er.pubmed}, Br = (r(233), r(81)), Wr = r(42), Jr = r(23), Hr = r(2), Vr = r(29),
        Ur = (r(234), Object(S.e)((() => {
            var e = M.a, t = Object.keys(Vr.a).reduce(((e, t) => (e.add(t.tag), e)), new Set).size > 1;
            return Object(a.jsxs)("div", {
                className: "ClusteringEngineSettings",
                children: [Object(a.jsx)("h4", {children: "Clustering algorithm"}), Object(a.jsx)(D.l, {
                    selectedValue: e.clusteringAlgorithm,
                    onChange: t => e.clusteringAlgorithm = t.currentTarget.value,
                    children: Object.keys(Vr.a).map((e => {
                        var r = Vr.a[e], n = "commercial" === r.tag, i = Object(a.jsxs)(a.Fragment, {
                            children: [Object(a.jsx)("strong", {children: r.label}), Object(a.jsx)(K, {
                                visible: t && !!r.tag,
                                content: () => Object(a.jsx)(D.q, {
                                    intent: n ? "warning" : "success",
                                    icon: n ? "dollar" : "git-branch",
                                    minimal: !0,
                                    children: r.tag
                                })
                            }), Object(a.jsx)("small", {children: r.description})]
                        });
                        return Object(a.jsx)(D.k, {label: i, value: e}, e)
                    }))
                }), Object(a.jsx)(y.b, {to: "/about", children: "more information"})]
            })
        }))), Qr = (r(235), Object(S.e)((e => {
            var t = Er[e.source];
            return Object(a.jsxs)("div", {
                className: "SearchEngineSettings",
                children: [Object(a.jsxs)("h4", {children: [t.label, " search options"]}), t.createSourceConfig({
                    onChange: () => {
                    }
                })]
            })
        }))), _r = r(64);

    function Gr(e) {
        return Object(a.jsx)(_r.a, {
            id: "sources",
            selectedTabId: e.active,
            onChange: e.onChange,
            className: "sources",
            children: Object.keys(Ar).map((e => Object(a.jsx)(D.o, {id: e, title: Ar[e].label}, e)))
        })
    }

    var Kr = ({initialQuery: e, source: t, onSourceChange: r, onSubmit: i}) => {
            var s = Object(n.useRef)(null), o = Object(n.useState)(e || ""), c = Object(h.a)(o, 2), l = c[0], u = c[1],
                d = () => {
                    s.current && s.current.focus()
                };
            Object(n.useEffect)(d, []);
            var m = () => {
                var e = l.trim();
                e.length > 0 && i(e)
            }, p = Object(a.jsxs)(Wr.a, {
                position: Jr.a.BOTTOM,
                className: Hr.a.FIXED,
                popoverClassName: "SearchAppSettingsContainer",
                children: [Object(a.jsx)(D.a, {
                    rightIcon: "caret-down",
                    text: "options",
                    minimal: !0,
                    title: "Search engine options"
                }), Object(a.jsx)(Qr, {source: t, onApply: m})]
            }), b = Object.keys(Vr.a).length < 2 ? null : Object(a.jsxs)(Wr.a, {
                position: Jr.a.RIGHT_TOP,
                className: Hr.a.FIXED,
                popoverClassName: "SearchAppSettingsContainer",
                children: [Object(a.jsx)(D.a, {
                    icon: Object(a.jsx)(P.a, {icon: Br.b}),
                    minimal: !0,
                    title: "Clustering algorithm"
                }), Object(a.jsx)(Ur, {})]
            });
            return Object(a.jsxs)("div", {
                className: "SearchForm",
                children: [Object(a.jsx)(Gr, {
                    active: t, onChange: (e, t, a) => {
                        a.preventDefault(), d(), r && r(e)
                    }
                }), Object(a.jsx)("form", {
                    onSubmit: e => {
                        e.preventDefault(), m()
                    },
                    children: Object(a.jsxs)(D.c, {
                        fill: !0,
                        children: [Object(a.jsx)(D.f, {
                            inputRef: s,
                            rightElement: p,
                            defaultValue: e,
                            onChange: e => u(e.target.value)
                        }), Object(a.jsx)(D.a, {
                            className: Hr.a.FIXED,
                            icon: Object(a.jsx)(P.a, {icon: Br.a}),
                            type: "submit",
                            text: "Search"
                        }), b]
                    })
                })]
            })
        }, Xr = ({match: e, history: t}) => {
            var r = decodeURIComponent(e.params.source), i = decodeURIComponent(e.params.query),
                s = Object(n.useCallback)((() => {
                    M.f.load(r, Er[r], i), document.title = i + (i.length > 0 ? " - " : "") + je.a.pageTitle
                }), [r, i]);
            Object(n.useEffect)((() => {
                s()
            }), [r, i, s]);
            var o = () => {
                var t = e.params.view;
                return t = t ? decodeURIComponent(t) : Object.keys(be)[0]
            }, c = e => {
                var r = u.a.searchResults.buildUrl(e);
                r === encodeURI(t.location.pathname) ? s() : t.push(r)
            };
            return Object(a.jsxs)("main", {
                className: "ResultsScreen",
                children: [Object(a.jsx)(Kr, {
                    initialQuery: i, source: r, onSourceChange: e => {
                        c({query: i, source: e, view: o()})
                    }, onSubmit: e => {
                        c({query: e, source: r, view: o()})
                    }
                }, i), Object(a.jsx)("div", {
                    className: "clusters",
                    children: Object(a.jsx)(w.a, {
                        activeView: o(), views: be, onViewChange: e => {
                            c({query: i, source: r, view: e})
                        }, children: Object(a.jsx)(k, {isLoading: () => M.d.loading})
                    })
                }), Object(a.jsx)("div", {
                    className: "docs",
                    children: Object(a.jsx)(w.a, {
                        views: ge, activeView: "list", onViewChange: () => {
                        }, source: Er[r], children: Object(a.jsx)(k, {isLoading: () => M.f.loading})
                    })
                })]
            })
        }, Yr = (r(236), ({
                              match: e,
                              history: t
                          }) => Er[e.params.source] ? Object(a.jsxs)("main", {
            className: "StartScreen",
            children: [je.a.createStartPageLogo(), Object(a.jsx)(Kr, {
                source: e.params.source, onSourceChange: e => {
                    t.push(u.a.searchStart.buildUrl({source: e}))
                }, onSubmit: r => {
                    t.push(u.a.searchResults.buildUrl({
                        query: r,
                        source: e.params.source,
                        view: Object.keys(be[0].views)[0]
                    }))
                }
            }), Object(a.jsx)("div", {
                className: "slogan",
                children: je.a.createSlogan()
            }), Object(a.jsxs)("div", {
                className: "WorkbenchHint",
                children: ["New! Try", " ", Object(a.jsxs)(y.c, {
                    to: u.a.workbench.path,
                    children: [Object(a.jsx)(P.a, {icon: l.l}), " Clustering Workbench"]
                }), " ", "to process data from local files, Solr, Elasticsearch."]
            })]
        }) : Object(a.jsx)(c.a, {to: u.a.searchStart.buildUrl({source: "web"})})), Zr = () => Object(a.jsx)(i.a.Fragment, {
            children: Object(a.jsx)("div", {
                className: "SearchApp",
                children: Object(a.jsx)(y.a, {
                    children: Object(a.jsxs)(c.d, {
                        children: [Object(a.jsx)(c.b, {
                            exact: !0,
                            path: u.a.searchStart.path,
                            component: Yr
                        }), Object(a.jsx)(c.b, {path: u.a.searchResults.path, component: Xr})]
                    })
                })
            })
        }), $r = (r(237), r(238), ({value: e, label: t}) => Object(a.jsxs)("div", {
            className: "Stat",
            children: [Object(a.jsx)("strong", {children: e}), Object(a.jsx)("small", {children: t})]
        })), ea = ({stats: e, divided: t}) => Object(a.jsx)("div", {
            className: C()("Stats", {WithDivider: t}),
            children: e.filter((e => void 0 !== e.value)).map((e => Object(a.jsx)($r, Object(T.a)({}, e), e.id)))
        }), ta = (r(239), ({logo: e, button: t, sideFixed: r, sideMain: n}) => Object(a.jsxs)("div", {
            className: "AppSide",
            children: [Object(a.jsxs)("div", {
                className: "AppSideFixed",
                children: [Object(a.jsxs)("div", {className: "AppSideHeader", children: [e, t]}), r]
            }), Object(a.jsx)("div", {className: "AppSideMain", children: n})]
        })), ra = Object(S.e)((({
                                    welcome: e,
                                    main: t,
                                    isInitial: r,
                                    stats: n,
                                    globalActions: i
                                }) => r ? Object(a.jsx)("div", {
            className: "AppMain AppWelcome",
            children: e
        }) : Object(a.jsxs)("div", {
            className: "AppMain",
            children: [Object(a.jsxs)("div", {className: "stats", children: [n, i]}), t]
        }))), aa = e => {
            var t = e.icon, r = e.children, n = Object(_.a)(e, ["icon", "children"]);
            return Object(a.jsx)(D.a, Object(T.a)(Object(T.a)({
                className: "AppMainButton",
                large: !0,
                intent: "primary",
                icon: Object(a.jsx)(P.a, {icon: t})
            }, n), {}, {children: r}))
        }, na = ({
                     className: e,
                     welcome: t,
                     logo: r,
                     button: n,
                     sideFixed: i,
                     sideMain: s,
                     stats: o,
                     globalActions: c,
                     main: l,
                     isInitial: u
                 }) => Object(a.jsxs)("div", {
            className: C()("AppWithSidePanel", e),
            children: [Object(a.jsx)(ta, {logo: r, button: n, sideFixed: i, sideMain: s}), Object(a.jsx)(ra, {
                welcome: t,
                main: l,
                isInitial: u,
                stats: o,
                globalActions: c
            })]
        }), ia = ({settings: e, get: t, set: r, defer: n = !1, timeout: i}) => n ? Object(a.jsx)(Wt, {
            className: "Settings",
            setting: e,
            set: r,
            get: t,
            timeout: i
        }) : Object(a.jsx)(Jt, {className: "Settings", setting: e, set: r, get: t}), sa = (e, t) => {
            e.forEach((e => {
                t(e), "group" === e.type && sa(e.settings, t)
            }))
        }, oa = (r(240), r(48)), ca = Object(S.e)((e => {
            var t = e.store, r = e.property, n = Object(_.a)(e, ["store", "property"]);
            return Object(a.jsx)(D.b, Object(T.a)(Object(T.a)({}, n), {}, {
                checked: t[r],
                onChange: e => t[r] = e.target.checked
            }))
        })), la = Object(z.b)("workbench:export:config", {format: "excel", includeClusters: !0, includeDocuments: !0}),
        ua = Object(S.e)((e => {
            var t = e.value, r = Object(_.a)(e, ["value"]), n = la.format === t;
            return Object(a.jsx)(D.a, Object(T.a)({
                active: n,
                intent: n ? oa.a.PRIMARY : oa.a.NONE,
                onClick: () => la.format = t
            }, r))
        })), da = Object(S.e)((() => Object(a.jsxs)(D.c, {
            className: "ExportFormatConfig",
            children: [Object(a.jsx)(ua, {value: "excel", text: "Excel"}), Object(a.jsx)(ua, {
                value: "openoffice",
                text: "OpenOffice"
            }), Object(a.jsx)(ua, {value: "csv", text: "CSV"}), Object(a.jsx)(ua, {value: "json", text: "JSON"})]
        }))), ha = Object(S.e)((() => Object(a.jsxs)("div", {
            className: "ExportOutputConfig",
            children: [Object(a.jsx)(ca, {
                label: "Clusters",
                store: la,
                property: "includeClusters"
            }), Object(a.jsx)(ca, {label: "Documents", store: la, property: "includeDocuments"})]
        }))), ma = Object(S.e)((() => Object(a.jsx)(D.a, {
            intent: oa.a.PRIMARY,
            onClick: ba,
            disabled: !la.includeDocuments && !la.includeClusters,
            children: "Export"
        }))),
        pa = () => Object(a.jsxs)("div", {children: [Object(a.jsx)("p", {children: "Choose the output format:"}), Object(a.jsx)(da, {}), Object(a.jsx)("p", {children: "Chose what to export:"}), Object(a.jsx)(ha, {}), Object(a.jsx)(ma, {})]}),
        ba = function () {
            var e = Object(rt.a)(tt.a.mark((function e() {
                return tt.a.wrap((function (e) {
                    for (; ;) switch (e.prev = e.next) {
                        case 0:
                            e.t0 = la.format, e.next = "json" === e.t0 ? 3 : "excel" === e.t0 ? 5 : "openoffice" === e.t0 ? 8 : "csv" === e.t0 ? 11 : 14;
                            break;
                        case 3:
                            return fa(), e.abrupt("break", 14);
                        case 5:
                            return e.next = 7, xa("xlsx");
                        case 7:
                            return e.abrupt("break", 14);
                        case 8:
                            return e.next = 10, xa("ods");
                        case 10:
                            return e.abrupt("break", 14);
                        case 11:
                            return e.next = 13, xa("csv");
                        case 13:
                            return e.abrupt("break", 14);
                        case 14:
                        case"end":
                            return e.stop()
                    }
                }), e)
            })));
            return function () {
                return e.apply(this, arguments)
            }
        }(), ga = () => M.d.documents.map((e => {
            e.__id, e.__rank, e.clusters;
            return Object(_.a)(e, ["__id", "__rank", "clusters"])
        })), ja = () => M.d.clusters.map((function e(t) {
            t.uniqueDocuments;
            var r = Object(_.a)(t, ["uniqueDocuments"]);
            return r.clusters && (r.clusters = r.clusters.map(e)), r
        })), fa = () => {
            var e = {};
            e = la.includeDocuments && la.includeClusters ? {
                documents: ga(),
                clusters: ja()
            } : la.includeDocuments ? ga() : ja(), Object(R.saveAs)(new Blob([JSON.stringify(e)], {type: "application/json"}), Object(M.b)("result", "json"))
        }, xa = function () {
            var e = Object(rt.a)(tt.a.mark((function e(t) {
                var a, n, i, s, o, c;
                return tt.a.wrap((function (e) {
                    for (; ;) switch (e.prev = e.next) {
                        case 0:
                            return e.next = 2, Promise.all([r.e(1), r.e(0)]).then(r.t.bind(null, 274, 7));
                        case 2:
                            a = e.sent, n = [], la.includeClusters ? (i = ga(), s = (e, t) => {
                                var r;
                                e.documents.forEach((r => {
                                    var a = {};
                                    t.forEach(((e, t) => {
                                        a["Cluster Level ".concat(t + 1)] = e.join(", ")
                                    })), a["Cluster Level ".concat(t.length + 1)] = e.labels.join(","), la.includeDocuments && Object.assign(a, i[r]), n.push(a)
                                }));
                                var a = [...t, e.labels];
                                null === (r = e.clusters) || void 0 === r || r.forEach((e => {
                                    s(e, a)
                                }))
                            }, M.d.clusters.forEach((e => {
                                s(e, [])
                            }))) : n = ga(), n.forEach((e => {
                                Object.keys(e).forEach((t => {
                                    Array.isArray(e[t]) && (e[t] = e[t].flat(Number.MAX_SAFE_INTEGER).join(", "))
                                }))
                            })), (o = a.utils.book_new()).Props = {
                                Title: "".concat(je.a.product, " Clustering Workbench results export"),
                                Author: "".concat(je.a.product, " Clustering Workbench"),
                                CreatedDate: new Date
                            }, c = a.utils.json_to_sheet(n), o.SheetNames.push("Export"), o.Sheets.Export = c, a.writeFile(o, Object(M.b)("result", t));
                        case 12:
                        case"end":
                            return e.stop()
                    }
                }), e)
            })));
            return function (t) {
                return e.apply(this, arguments)
            }
        }(), va = () => Object(a.jsxs)(Wr.a, {
            className: "Export",
            boundary: "viewport",
            children: [Object(a.jsx)(D.a, {
                minimal: !0,
                small: !0,
                text: "Export",
                open: !0,
                icon: Object(a.jsx)(P.a, {icon: l.k})
            }), Object(a.jsx)(pa, {})]
        }), Oa = r(56), ya = (r(241), Object(S.e)((({label: e, id: t, components: r, get: n, set: i}) => {
            var s = "workbench-".concat(t);
            return Object(a.jsx)(D.d, {
                label: e,
                labelFor: s,
                inline: !0,
                children: Object(a.jsx)(D.e, {
                    value: n(), onChange: e => {
                        i(e.target.value)
                    }, id: s, fill: !0, children: Object.keys(r).map((e => {
                        var t = r[e];
                        return Object(a.jsx)("option", {value: e, children: t.label}, e)
                    }))
                })
            })
        }))), wa = () => Object(a.jsxs)("div", {
            className: "WorkbenchSourceAlgorithm",
            children: [Object(a.jsx)(ya, {
                label: "Data source",
                id: "source",
                components: Er,
                get: () => jr.source,
                set: e => jr.source = e
            }), Object(a.jsx)(ya, {
                label: "Clustering algorithm",
                id: "algorithm",
                components: Vr.a,
                get: () => M.a.clusteringAlgorithm,
                set: e => M.a.clusteringAlgorithm = e
            })]
        }), Sa = (r(242), r(66)), Fa = Object(z.b)("workbench:parameterExport:config", {onlyNonDefault: !0}),
        Ca = Object(S.e)((() => {
            var e = Object(M.c)(Fa.onlyNonDefault), t = JSON.stringify(e, null, "  ");
            return Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)("h4", {children: "Clustering parameters JSON"}), Object(a.jsxs)("div", {
                    className: "ExportParametersTools",
                    children: [Object(a.jsx)(ca, {
                        label: "Include only non-default",
                        store: Fa,
                        property: "onlyNonDefault"
                    }), Object(a.jsx)(Sa.a, {contentProvider: () => t})]
                }), Object(a.jsx)(it, {jsonString: t})]
            })
        })), ka = () => Object(a.jsxs)(Wr.a, {
            position: Jr.a.TOP_LEFT,
            popoverClassName: "ExportParameters",
            children: [Object(a.jsx)(D.a, {
                icon: Object(a.jsx)(P.a, {icon: l.b}),
                title: "Clustering parameters as JSON",
                small: !0
            }), Object(a.jsx)(Ca, {})]
        }), Ta = {
            id: "root",
            settings: [{components: Er, type: "source"}, {
                components: Vr.a,
                type: "algorithm"
            }].map((e => Object.keys(e.components).map((t => {
                var r = e.components[t].getSettings();
                return r.forEach((r => {
                    r.visible = r => {
                        switch (e.type) {
                            case"source":
                                return t === jr.source;
                            case"algorithm":
                                return t === M.a.clusteringAlgorithm;
                            default:
                                return !1
                        }
                    }
                })), r
            })))).flat(2)
        }, La = ((e, t) => {
            var r = Object(z.b)(t, {}), a = e => r[e.id], n = [];
            sa(e, (e => {
                "group" !== e.type || Object(st.d)(e.label) || (n.push(e), e.folded = () => a(e), e.onHeaderClick = () => {
                    ((e, t) => {
                        r[e.id] = t
                    })(e, !a(e))
                })
            }));
            var i = e => {
                n.forEach((t => {
                    r[t.id] = e
                }))
            };
            return {isAllFolded: () => n.every((e => r[e.id])), foldAll: () => i(!0), expandAll: () => i(!1)}
        })(Ta.settings, "workbench:settings:folding"), Ia = La.isAllFolded, za = La.foldAll, qa = La.expandAll,
        Na = Object(S.d)({sourceDirty: !1, algorithmDirty: !1}), Ra = e => {
            Object.keys(e).forEach((t => {
                var r;
                e[t].getSettings().reduce((function e(t, a) {
                    if ("group" === a.type) r || (r = a.get), a.settings.reduce(e, []); else if (a.get || r) {
                        var n = (a.get || r)(a);
                        if ("function" === typeof (null === n || void 0 === n ? void 0 : n.forEach)) {
                            var i = 0;
                            n.forEach((e => i++))
                        }
                    }
                    return t
                }), [])
            }))
        };
    Object(S.a)((() => {
        Object(S.b)((() => {
            Ra(Er);
            var e = !!jr.source;
            Na.sourceDirty = e || !0
        }))
    })), Object(S.a)((() => {
        Object(S.b)((() => {
            Ra(Vr.a);
            var e = !!M.a.clusteringAlgorithm;
            Na.algorithmDirty = e || !0
        }))
    }));
    var Da, Pa = Object(z.b)("workbench:settings:state", {showAdvancedSettings: !1}),
        Ma = Object(S.e)((() => Object(a.jsx)(D.a, {
            icon: Object(a.jsx)(P.a, {icon: l.a}),
            title: "Show advanced settings",
            small: !0,
            active: Pa.showAdvancedSettings,
            onClick: () => Pa.showAdvancedSettings = !Pa.showAdvancedSettings
        }))), Ea = Object(S.e)((() => {
            var e = Ia();
            return Object(a.jsx)(D.a, {
                icon: Object(a.jsx)(P.a, {icon: e ? l.j : l.g}),
                title: "".concat(e ? "Expand" : "Fold", " all setting groups"),
                small: !0,
                onClick: () => e ? qa() : za()
            })
        })), Aa = () => Object(a.jsxs)("div", {
            className: "SettingsTools",
            children: [Object(a.jsx)(D.a, {
                icon: Object(a.jsx)(P.a, {icon: l.w}),
                title: "Reset all settings to defaults",
                small: !0,
                onClick: M.a.getAlgorithmInstance().resetToDefaults
            }), Object(a.jsx)(Ma, {}), Object(a.jsx)(Ea, {}), Object(a.jsx)(ka, {})]
        });
    Da = () => Pa.showAdvancedSettings, sa(Ta.settings, (e => {
        if (e.advanced) {
            var t = e.visible;
            e.visible = () => (e.advanced || !1) === Da() && (!t || t())
        }
    }));
    var Ba = () => {
            Na.sourceDirty ? M.f.load(jr.source, Er[jr.source], ye.query) : Object(M.e)(), Na.algorithmDirty = !1, Na.sourceDirty = !1
        }, Wa = (r(243), Object(S.e)((() => {
            var e, t = Er[jr.source], r = null === (e = t.createIntroHelp) || void 0 === e ? void 0 : e.call(t);
            return Object(a.jsxs)("li", {
                className: "SourceConfiguration",
                children: [Object(a.jsxs)("h3", {children: ["Configure ", Object(a.jsx)("strong", {children: t.label}), " data source"]}), r]
            })
        }))), Ja = ({source: e, children: t}) => Object(a.jsx)(G.a, {onClick: () => jr.source = e, children: t}),
        Ha = () => Object(a.jsx)("ul", {
            children: Object.keys(Er).map((e => Object(a.jsx)("li", {
                children: Object(a.jsx)(Ja, {
                    source: e,
                    children: Er[e].contentSummary
                })
            }, e)))
        }), Va = () => Object(a.jsx)("div", {
            className: "WorkbenchIntroSteps",
            children: Object(a.jsxs)("ol", {
                children: [Object(a.jsxs)("li", {
                    className: "SourceAlgorithmChoice",
                    children: [Object(a.jsx)("h3", {children: "Choose data source:"}), Object(a.jsx)(Ha, {})]
                }), Object(a.jsx)(Wa, {}), Object(a.jsx)("li", {
                    className: "ButtonPress",
                    children: Object(a.jsxs)("h3", {children: ["Press the ", Object(a.jsx)("strong", {children: "Cluster"}), " button"]})
                })]
            })
        }), Ua = () => Object(a.jsxs)(a.Fragment, {
            children: [Object(a.jsxs)("div", {
                className: "WorkbenchIntroWelcome",
                children: [Object(a.jsx)("h2", {children: "Welcome to Clustering Workbench"}), Object(a.jsxs)("h3", {children: ["the expert-level ", je.a.createProductName(), " application"]})]
            }), Object(a.jsx)(Va, {})]
        }), Qa = () => Object(a.jsx)("div", {
            className: "WorkbenchLogo",
            children: Object(a.jsxs)("span", {
                children: [Object(a.jsx)("span", {children: "clustering"}), Object(a.jsx)("span", {
                    className: "initial",
                    children: "W"
                }), "orkbench"]
            })
        }), _a = Object(S.e)((() => (Object(n.useEffect)((() => {
            var e = e => {
                13 !== e.keyCode && 10 !== e.keyCode || !e.ctrlKey || Ba()
            };
            return window.addEventListener("keypress", e), () => window.removeEventListener("keypress", e)
        }), []), Object(a.jsx)(aa, {
            intent: Na.sourceDirty || Na.algorithmDirty ? "primary" : "none",
            icon: l.r,
            title: "Press Ctrl+Enter to perform clustering",
            onClick: Ba,
            loading: M.f.loading || M.d.loading,
            children: "Cluster"
        })))), Ga = Object(S.e)((() => {
            var e, t = [{id: "result-count", value: M.f.searchResult.documents.length, label: "results"}, {
                id: "cluster-count",
                value: M.d.clusters.length,
                label: "clusters"
            }, {
                id: "clustered-docs",
                value: (100 * M.d.getClusteredDocsRatio()).toFixed(1) + "%",
                label: "clustered docs"
            }, {
                id: "processing-time",
                value: Object(Y.b)(null === (e = M.d.serviceInfo) || void 0 === e ? void 0 : e.clusteringTimeMillis),
                label: "clustering time"
            }];
            return Object(a.jsx)(ea, {stats: t})
        })), Ka = Object(S.e)((() => Object(a.jsxs)(a.Fragment, {
            children: [Object(a.jsx)("div", {
                className: "clusters",
                children: Object(a.jsx)(w.a, {
                    activeView: Oa.a.clusterView,
                    views: be,
                    onViewChange: e => Oa.a.clusterView = e,
                    children: Object(a.jsx)(k, {
                        isLoading: () => {
                            var e, t = be[0].views[Oa.a.clusterView];
                            return M.f.loading || M.d.loading || (null === (e = t.isLoading) || void 0 === e ? void 0 : e.call(t))
                        }
                    })
                })
            }), Object(a.jsx)("div", {
                className: "docs",
                children: Object(a.jsx)(w.a, {
                    views: ge, activeView: "list", onViewChange: () => {
                    }, source: Er[jr.source], children: Object(a.jsx)(k, {isLoading: () => M.f.loading})
                })
            })]
        }))), Xa = Object(S.e)((() => Object(a.jsx)(na, {
            className: "WorkbenchApp",
            isInitial: M.f.initial,
            welcome: Object(a.jsx)(Ua, {}),
            logo: Object(a.jsx)(Qa, {}),
            button: Object(a.jsx)(_a, {}),
            sideFixed: Object(a.jsxs)(a.Fragment, {children: [Object(a.jsx)(wa, {}), Object(a.jsx)(Aa, {})]}),
            sideMain: Object(a.jsx)(ia, {settings: Ta, defer: !0}),
            stats: Object(a.jsx)(Ga, {}),
            globalActions: Object(a.jsx)(va, {}),
            main: Object(a.jsx)(Ka, {})
        }))),
        Ya = (r(244), () => Object(a.jsx)(a.Fragment, {children: Object(a.jsx)("ul", {children: Object.keys(Er).map((e => Object(a.jsxs)("li", {children: [Object(a.jsx)("strong", {children: Er[e].label}), ":\xa0", Object(a.jsx)("span", {dangerouslySetInnerHTML: {__html: Er[e].descriptionHtml}})]}, e)))})})),
        Za = () => Object(a.jsx)(a.Fragment, {
            children: Object(a.jsx)("ul", {
                children: Object.keys(Vr.a).map((e => Object(a.jsxs)("li", {
                    style: {breakInside: "avoid"},
                    children: [Object(a.jsx)("strong", {children: Vr.a[e].label}), ":\xa0", Object(a.jsx)("span", {dangerouslySetInnerHTML: {__html: Vr.a[e].descriptionHtml}})]
                }, e)))
            })
        }), $a = () => Object(a.jsx)("div", {
            className: "VersionInfo",
            children: Object(a.jsxs)("ul", {children: [Object(a.jsxs)("li", {children: [Object(a.jsx)("span", {children: "version:"}), " ", "4.2.1"]}), Object(a.jsxs)("li", {children: [Object(a.jsx)("span", {children: "build date:"}), " ", "2021-03-29T11:00+02:00"]}), Object(a.jsxs)("li", {children: [Object(a.jsx)("span", {children: "git rev:"}), " ", "936bcf7fa48e03fafffdf4e6f15b36074d161e6e"]})]})
        }), en = () => Object(a.jsxs)("div", {
            className: "SearchAppInfo",
            children: [Object(a.jsxs)("h2", {children: [je.a.createProductName(), " clustering engine"]}), Object(a.jsxs)("main", {children: [je.a.createAboutIntro(), Object(a.jsx)("h3", {children: "Search engines"}), Object(a.jsx)(Ya, {}), Object(a.jsx)("h3", {children: "Clustering algorithms"}), Object(a.jsx)(Za, {}), je.a.createAboutDetails(), Object(a.jsx)($a, {})]})]
        }), tn = () => Object(a.jsxs)(d.b, {
            containerClassName: e => Object(c.f)(e.pathname, {
                path: u.a.searchStart.path,
                exact: !0
            }) ? "WithBackdrop" : null,
            children: [je.a.createAppLogo(), Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)(d.a, {
                    path: u.a.search.path,
                    title: "Web search clustering",
                    icon: l.v,
                    component: Zr,
                    default: !0,
                    children: Object(a.jsx)("p", {children: "Clustering of search results from public search engines."})
                }), Object(a.jsx)(d.a, {
                    path: u.a.workbench.path,
                    title: "Clustering workbench",
                    icon: l.l,
                    component: Xa,
                    children: Object(a.jsxs)("ul", {
                        className: "WorkbenchLinkPopover",
                        children: [Object(a.jsx)("li", {children: "clustering data from files, Solr, Elasticsearch"}), Object(a.jsx)("li", {children: "experimenting with clustering parameters"}), Object(a.jsx)("li", {children: "exporting results to Excel/OpenOffice"})]
                    })
                })]
            }), Object(a.jsxs)(a.Fragment, {
                children: [Object(a.jsx)(d.a, {
                    path: u.a.about.path,
                    title: "About this application",
                    icon: l.o,
                    component: en
                }), je.a.createAppInfoNavLink()]
            }), Object(a.jsxs)(c.d, {
                children: [Object(a.jsx)(c.b, {
                    exact: !0,
                    path: u.a.searchStart.path,
                    component: O
                }), Object(a.jsx)(c.b, {exact: !0, path: u.a.about.path, component: O})]
            })]
        });
    Boolean("localhost" === window.location.hostname || "[::1]" === window.location.hostname || window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));
    o.a.render(Object(a.jsx)(tn, {}), document.getElementById("root")), "serviceWorker" in navigator && navigator.serviceWorker.ready.then((e => {
        e.unregister()
    }))
}, , , , function (e, t, r) {
    "use strict";
    r.d(t, "a", (function () {
        return a
    })), r.d(t, "b", (function () {
        return n
    }));
    var a = {
        "caret-down": ["M12 6.5c0-.28-.22-.5-.5-.5h-7a.495.495 0 0 0-.37.83l3.5 4c.09.1.22.17.37.17s.28-.07.37-.17l3.5-4c.08-.09.13-.2.13-.33z"],
        "chevron-down": ["M12 5c-.28 0-.53.11-.71.29L8 8.59l-3.29-3.3a1.003 1.003 0 0 0-1.42 1.42l4 4c.18.18.43.29.71.29s.53-.11.71-.29l4-4A1.003 1.003 0 0 0 12 5z"],
        "chevron-up": ["M12.71 9.29l-4-4C8.53 5.11 8.28 5 8 5s-.53.11-.71.29l-4 4a1.003 1.003 0 0 0 1.42 1.42L8 7.41l3.29 3.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71z"],
        cross: ["M11.41 10l4.29-4.29c.19-.18.3-.43.3-.71a1.003 1.003 0 0 0-1.71-.71L10 8.59l-4.29-4.3a1.003 1.003 0 0 0-1.42 1.42L8.59 10 4.3 14.29c-.19.18-.3.43-.3.71a1.003 1.003 0 0 0 1.71.71l4.29-4.3 4.29 4.29c.18.19.43.3.71.3a1.003 1.003 0 0 0 .71-1.71L11.41 10z"],
        "small-cross": ["M9.41 8l2.29-2.29c.19-.18.3-.43.3-.71a1.003 1.003 0 00-1.71-.71L8 6.59l-2.29-2.3a1.003 1.003 0 00-1.42 1.42L6.59 8 4.3 10.29c-.19.18-.3.43-.3.71a1.003 1.003 0 001.71.71L8 9.41l2.29 2.29c.18.19.43.3.71.3a1.003 1.003 0 00.71-1.71L9.41 8z"],
        "double-caret-vertical": ["M5 7h6a1.003 1.003 0 0 0 .71-1.71l-3-3C8.53 2.11 8.28 2 8 2s-.53.11-.71.29l-3 3A1.003 1.003 0 0 0 5 7zm6 2H5a1.003 1.003 0 0 0-.71 1.71l3 3c.18.18.43.29.71.29s.53-.11.71-.29l3-3A1.003 1.003 0 0 0 11 9z"]
    }, n = {}
}], [[245, 7, 9]], [11, 4, 12, 8]]);
//# sourceMappingURL=main.4974e0c5.chunk.js.map