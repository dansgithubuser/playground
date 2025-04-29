import gdsfactory as gf

@gf.cell
def sample_pcell(size=1, name="world") -> gf.Component:
    c = gf.Component()
    ref1 = c.add_ref(gf.components.rectangle(size=(10, 10), layer=(1, 0)))
    ref2 = c.add_ref(gf.components.text("Hello", size=size, layer=(2, 0)))
    ref3 = c.add_ref(gf.components.text(name, size=size, layer=(2, 0)))
    ref1.xmax = ref2.xmin - 5
    ref3.xmin = ref2.xmax + 2
    ref3.rotate(90)
    return c

c = sample_pcell()
c.write_gds('hello.gds')
