import common
import product


def test_simple_product():
    process = common.process_example()
    environment = common.environment_example()
    p = product.Product([process, environment])
    print p
    for s in p.nodes():
        print s
    assert 'p0,e0' in p.nodes()
    assert ('p0,e0', 'p1,e1', {'label': 'a!oh'}) in p.edges(data=True),\
        "'a' should appear as an output of the product"
