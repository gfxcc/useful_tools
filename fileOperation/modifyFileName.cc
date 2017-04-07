#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include <vector>
#include <string>
#include <iostream>
#include <ctype.h>
#include <stdio.h>

using namespace std;

/*function... might want it in some class?*/
int getdir (string dir, vector<string> &files)
{
    DIR *dp;
    struct dirent *dirp;
    if((dp  = opendir(dir.c_str())) == NULL) {
        cout << "Error(" << errno << ") opening " << dir << endl;
        return errno;
    }

    while ((dirp = readdir(dp)) != NULL) {
        string file(dirp->d_name);
        string type, name;
        size_t pos;
        if ((pos = file.find_last_of(".")) == string::npos)
            continue;

        name = file.substr(0, pos);
        type = file.substr(pos + 1);
        if (type != "mp3")
            continue;
        files.push_back(file);
    }
    closedir(dp);
    return 0;
}

int main()
{
    string dir = string(".");
    vector<string> files, new_names;

    getdir(dir,files);

    for (auto file : files) {
        size_t pos = 0;
        while (!isdigit(file[pos]))
            pos++;
        string new_name = file.substr(pos, 3) + ".mp3";
        new_names.push_back(new_name);
    }

    cout << files.size() << " files going to be renamed: " << endl;
    
    for (size_t i = 0; i < files.size(); i++) {
        cout << files[i] << " ->" << new_names[i] << endl;
    }

    cout << "Press Y to continues:" << endl;
    char f = getchar();
    if (f != 'Y')
        return 0;

    for (size_t i = 0; i < files.size(); i++) {
        if (rename(files[i].c_str(), new_names[i].c_str()) != 0)
            cout << "error" << endl;
    }
    return 0;
}
