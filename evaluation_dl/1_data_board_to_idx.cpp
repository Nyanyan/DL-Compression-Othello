#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <fstream>
#include "evaluation_definition.hpp"

#define ADJ_N_FEATURES_DNN 224 // raw: 1342

#define N_DATA_PER_FILE 8192 //16384

int main(int argc, char *argv[]){
    if (argc < 6){
        std::cerr << "input [input dir] [start file no] [n files] [output dir] [phase]" << std::endl;
        return 1;
    }

    evaluation_definition_init();

    int t = 0;

    int start_file = atoi(argv[2]);
    int n_files = atoi(argv[3]);
    //int phase = atoi(argv[5]);

    std::string output_dir = argv[4];

    int file_sub = 0;
    int n_board = 0;

    std::ofstream fout;

    Board board;
    int8_t player, score, policy, phase;
    int8_t score_char;
    uint8_t idxes_dnn[ADJ_N_FEATURES_DNN];
    FILE* fp;
    std::string file;
    for (int i = start_file; i < n_files; ++i){
        std::cerr << "=";
        file = std::string(argv[1]) + "/" + std::to_string(i) + ".dat";
        if (fopen_s(&fp, file.c_str(), "rb") != 0) {
            std::cerr << "can't open " << file << std::endl;
            continue;
        }
        while (true){
            if (fread(&(board.player), 8, 1, fp) < 1)
                break;
            fread(&(board.opponent), 8, 1, fp);
            fread(&player, 1, 1, fp);
            fread(&policy, 1, 1, fp);
            fread(&score, 1, 1, fp);
            //if (calc_phase(&board, player) == phase){
            if (n_board == N_DATA_PER_FILE){
                fout.close();
                n_board = 0;
                ++file_sub;
            }
            if (n_board == 0){
                std::cerr << output_dir + "/" + std::to_string(file_sub) + ".dat" << std::endl;
                fout.open(output_dir + "/" + std::to_string(file_sub) + ".dat", std::ios::out|std::ios::binary|std::ios::trunc);
                if (!fout){
                    std::cerr << "can't open" << std::endl;
                    return 1;
                }
            }
            score_char = score + 64; // to avoid 8 bit signed
            adj_calc_features_dnn(&board, idxes_dnn);
            phase = calc_phase(&board, player);
            fout.write((char*)&phase, 1);
            fout.write((char*)idxes_dnn, 1 * ADJ_N_FEATURES_DNN);
            fout.write((char*)&score_char, 1);
            ++t;
            ++n_board;
            //}
        }
        if (i % 20 == 19)
            std::cerr << std::endl;
    }
    std::cerr << t << std::endl;
    return 0;

}