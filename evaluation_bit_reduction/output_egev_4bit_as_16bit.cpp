#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <ios>
#include <iomanip>

#define EVAL_MAX 4091
//#define SIMD_EVAL_OFFSET 4092

int main(int argc, char* argv[]){
    std::ofstream fout;
    fout.open("eval_4bit_as_16bit.egev", std::ios::out|std::ios::binary|std::ios::trunc);
    if (!fout){
        std::cerr << "can't open eval.egev" << std::endl;
        return 1;
    }
    short elem;
    short max_elem = -4091, min_elem = 4091;
    std::ifstream ifs("txt_eval_4bit_joined.txt");
    if (ifs.fail()){
        std::cerr << "ERR" << std::endl;
        return 0;
    }
    std::string line;
    int t = 0;
    while (std::getline(ifs, line)){
        int elem_int = stoi(line) * 256;
        if (elem_int > EVAL_MAX)
            elem_int = EVAL_MAX;
        else if (elem_int < -EVAL_MAX)
            elem_int = -EVAL_MAX;
        elem = (short)elem_int;
        max_elem = std::max(max_elem, elem);
        min_elem = std::min(min_elem, elem);
        //elem += SIMD_EVAL_OFFSET;
        fout.write((char*)&elem, 2);
        ++t;
    }
    std::cerr << "EVAL_MAX " << EVAL_MAX << std::endl;
    std::cerr << "min " << min_elem << std::endl;
    std::cerr << "max " << max_elem << std::endl;
    std::cerr << "done" << std::endl;

    return 0;
}