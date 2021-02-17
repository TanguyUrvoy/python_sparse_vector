#include <boost/python.hpp>
#include "SparseVec.hpp" 

using namespace boost::python;

BOOST_PYTHON_MODULE(sparse_vector)
{
    class_< SparseVec<float> >("SparseVec", init<std::string>())
    .def(init< list >())
    .def("__repr__", &SparseVec<float>::repr)
    .def("__setitem__", &SparseVec<float>::set_item)
    .def("__getitem__", &SparseVec<float>::get_item)
    .def("__iadd__", &SparseVec<float>::iadd)
    .def("__add__", &SparseVec<float>::add)
    .def("__isub__", &SparseVec<float>::isub)
    .def("__sub__", &SparseVec<float>::sub)
    .def("__imul__", &SparseVec<float>::isub)
    .def("__mul__", &SparseVec<float>::sub)
    .def("__eq__", &SparseVec<float>::eq)
    .def("__ne__", &SparseVec<float>::neq)
    .def("__le__", &SparseVec<float>::leq)
    .def("__ge__", &SparseVec<float>::geq)
    .def("__lt__", &SparseVec<float>::lt)
    .def("__gt__", &SparseVec<float>::gt)
    ;
    
}


