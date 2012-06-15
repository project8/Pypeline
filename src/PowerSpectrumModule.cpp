#include <iostream>

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>

using namespace std;
using namespace boost::python;

// Functions will go here
void make_spectrum(const char* filename) {
}

BOOST_PYTHON_MODULE(PowerSpectrum)
// Here the methods/functions are added to the module (must be defined above)
{
    def("make_spectrum", make_spectrum);
}
