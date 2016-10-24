from unclutter import remove_clutter


def test0():
    text = 'foo'
    res = remove_clutter(text)
    assert res == 'foo'


def test1():
    text = '''<span><style>.YZgB{display:none}.XKbo{display:inline}.PoDB{display:none}.Pv1X{display:inline}.cH4_{display:none}.kXn-{display:inline}</style><span class="YZgB">32</span><span></span><span class="PoDB">147</span><div style="display:none">147</div><span style="display:none">170</span><div style="display:none">170</div><div style="display:none">194</div><span class="21">223</span><span style="display:none">232</span><span class="cH4_">232</span><div style="display:none">232</div><span style="display:none">242</span><span class="cH4_">242</span><span style="display:none">249</span><div style="display:none">249</div><span class="cH4_">250</span><div style="display:none">250</div><span class="216">.</span><span class="XKbo">16</span><span style="display: inline">.</span><div style="display:none">131</div><span style="display:none">224</span><span class="cH4_">224</span><div style="display:none">224</div><span class="XKbo">231</span><span style="display:none">239</span><div style="display:none">239</div><span class="149">.</span><span></span>135<span style="display:none">182</span><span class="YZgB">182</span><span style="display:none">217</span></span>'''
    res = remove_clutter(text)
    assert res == '223.16.231.135'
