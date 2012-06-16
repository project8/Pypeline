#include <iostream>

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>

#include "KTEgg.hh"
#include "KTEvent.hh"
#include "KTPowerSpectrum.hh"
#include "KTSimpleFFT.hh"
#include "KTArrayUC.hh"
#include "TCanvas.h"

using namespace std;
using namespace boost::python;

// Functions will go here
void make_spectrum(const char* filename) {
    cout << "name of file is: " << filename << "!\n";

    Katydid::KTEgg* egg = new Katydid::KTEgg();
    egg->SetFileName(filename);
    if (! egg->BreakEgg()) {
        cout << "ERROR: Egg did not break" << endl;
    }
    if (! egg->ParseEggHeader()) {
        cout << "ERROR: Header did not parse" << endl;
        return;
    }

    while (kTRUE) {
        // Hatch the event
        Katydid::KTEvent* event = egg->HatchNextEvent();
        if (event == NULL) {
            std::cout << "ERROR: Event did not hatch" << std::endl;
            break;
        }

        TCanvas* c1 = new TCanvas("c1", "c1");
        c1->cd();
        TH1I* histAmpDist = event->CreateAmplitudeDistributionHistogram();
        histAmpDist->Draw();

        Katydid::KTSimpleFFT* fft = new Katydid::KTSimpleFFT((Int_t)event->GetRecord()->GetSize());
        fft->SetTransformFlag("ES");
        fft->InitializeFFT();
        fft->TakeData(event);
        fft->Transform();

        Katydid::KTPowerSpectrum* ps = fft->CreatePowerSpectrum();
        delete fft;
        TH1D* histPowerSpect = ps->CreateMagnitudeHistogram();
        TH1D* histPowerDist = ps->CreatePowerDistributionHistogram();
        delete ps;

        TCanvas* c2 = new TCanvas("c2", "c2");
        c2->cd();
        c2->SetLogy(1);
        histPowerSpect->Draw();

        TCanvas* c3 = new TCanvas("c3", "c3");
        c3->cd();
        c3->SetLogy(1);
        histPowerDist->Draw();

        c3->WaitPrimitive();

        delete c1;
        delete c2;
        delete c3;

    }
}

BOOST_PYTHON_MODULE(PowerSpectrum)
// Here the methods/functions are added to the module (must be defined above)
/*from the docs the def overloads are:
    def("name", function_ptr);
    def("name", function_ptr, call_policies);
    def("name", function_ptr, "documentation string");
    def("name", function_ptr, call_policies, "documentation string");
    */
{
    def("make_spectrum", make_spectrum);
}
