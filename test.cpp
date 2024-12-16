#include <iostream>
#include "CLI11.hpp"
#include <curl/curl.h>
#include "json.hpp"
#include <random>
#include <filesystem>

using json = nlohmann::json;
using namespace std;

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, string *output)
{
    size_t totalSize = size * nmemb;
    output->append((char *)contents, totalSize);
    return totalSize;
}

string parseHeadline(const json &item)
{
    string headline = item["headline"].get<string>();
    string url = item["url"].get<string>();

    size_t pos = 0;
    while ((pos = headline.find("&#39;", pos)) != string::npos)
    {
        headline.replace(pos, 5, "'");
        pos += 1;
    }

    return "- \033]8;;" + url + "\033\\" + headline + "\033]8;;\033\\\n";
}

vector<string> getCategoryNews(const string &category, const json &newsData)
{
    if (newsData.contains(category))
    {
        vector<string> headlines;
        for (const auto &item : newsData[category])
        {
            string s = parseHeadline(item);
            headlines.push_back(s);
        }
        return headlines;
    }

    return vector<string>();
}

vector<string> getRandomHeadlines(json newsData, int num)
{
    ifstream in("cats.txt");
    string category;
    vector<string> categories;
    while (in >> category)
    {
        categories.push_back(category);
    }

    vector<string> ret;

    random_device dev;
    mt19937 rng(dev());
    uniform_int_distribution<mt19937::result_type> rand1(0, categories.size());

    for (int i = 0; i < num; i++)
    {
        int index = rand1(rng);
        vector<string> headlines = getCategoryNews(categories[index], newsData);
        if (!headlines.empty())
        {
            uniform_int_distribution<mt19937::result_type> rand2(0, headlines.size());
            int j = rand2(rng);
            ret.push_back(headlines[j]);
        }
    }

    in.close();

    return ret;
}

string getCurrentTime()
{
    string format = "%Y-%m-%d-%H-%M";
    time_t now = time(0);
    tm *now_tm = gmtime(&now);
    char buf[42];
    strftime(buf, 42, "%Y-%m-%d-%H-%M", now_tm);

    return buf;
}

bool fetchGitHubNewsFile(string &fileContent)
{
    string current_time = getCurrentTime();

    ifstream fileStream;
    fileStream.open("results/result.json");
    if (!fileStream.fail())
    {
        json newsData = json::parse(fileStream);

        string save_time = newsData["time"].get<string>();

        tm tm1 = {};
        stringstream ss1(save_time);
        ss1 >> std::get_time(&tm1, "%Y-%m-%d-%H-%M");
        tm1.tm_mday += 1;
        time_t t1 = mktime(&tm1);

        tm tm2 = {};
        stringstream ss2(current_time);
        ss2 >> get_time(&tm2, "%Y-%m-%d-%H-%M");
        time_t t2 = mktime(&tm2);


        if (t2 < t1)
        {
            // cout<<"UPDATE"<<endl;
            fileStream.close();
            fileContent = newsData.dump();
            return true;
        }
        fileStream.close();
    }

    CURL *curl;
    CURLcode res;
    string readBuffer;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (!curl)
    {
        cerr << "Failed to initialize curl" << endl;
        return false;
    }

    const string url = "https://api.github.com/repos/kevins4202/cli/contents/results/result.json?ref=main";

    struct curl_slist *headers = nullptr;
    headers = curl_slist_append(headers, "Accept: application/vnd.github.v3.raw");
    headers = curl_slist_append(headers, "User-Agent: CLI-App");

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 1L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 2L);

    // Perform the request
    res = curl_easy_perform(curl);

    // Check for errors
    if (res != CURLE_OK)
    {
        cerr << "Curl request failed: " << curl_easy_strerror(res) << endl;
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
        return false;
    }

    // Clean up
    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);
    curl_global_cleanup();

    // Store the file content
    fileContent = readBuffer;
    json newsData = json::parse(fileContent);
    ofstream file("results/result.json");
    file << newsData.dump();
    file.close();

    return true;
}

// Function to print "hello"
void printHello()
{
    cout << "Hello!" << endl;
}

int main(int argc, char **argv)
{
    CLI::App app{"News CLI Application"};

    // Ensure UTF-8 compatibility
    argv = app.ensure_utf8(argv);

    // Option for file name
    string filename = "default";
    app.add_option("-f,--file", filename, "Specify a file name");

    // Change the short flag for hello to -H
    bool helloFlag = false;
    app.add_flag("-H,--hello", helloFlag, "Print 'hello'");

    bool news_mode = false;
    bool business = false, entertainment = false, politics = false, tech = false, science = false, sports = false, us = false, world = false;

    auto *news_opt = app.add_flag("-N,--news", news_mode, "Enable news mode");
    auto *news_group = app.add_option_group("News Categories");
    news_group->add_flag("--tech", tech, "Show technology news")->needs(news_opt);
    news_group->add_flag("--business", business, "Show business news")->needs(news_opt);
    news_group->add_flag("--science", science, "Show science news")->needs(news_opt);
    news_group->add_flag("--sports", sports, "Show sports news")->needs(news_opt);
    news_group->add_flag("--entertainment", entertainment, "Show entertainment news")->needs(news_opt);
    news_group->add_flag("--politics", politics, "Show politics news")->needs(news_opt);
    news_group->add_flag("--us", us, "Show US news")->needs(news_opt);
    news_group->add_flag("--world", world, "Show world news")->needs(news_opt);

    // Parse arguments
    CLI11_PARSE(app, argc, argv);

    // Perform actions based on flags
    if (helloFlag)
    {
        printHello();
    }

    if (filename != "default")
    {
        cout << "File name: " << filename << endl;
    }

    if (!news_mode)
    {
        return 0;
    }

    string jsonContent;
    if (!fetchGitHubNewsFile(jsonContent))
    {
        return 1;
    }

    try
    {
        json newsData = json::parse(jsonContent);

        // If no flags are set, show 10 random headlines
        if (!tech && !business && !science && !sports && !entertainment && !politics && !us && !world)
        {
            cout << "\n=== Random Headlines ===" << endl
                 << endl;

            for (const auto &headline : getRandomHeadlines(newsData, 10))
            {
                cout << headline << endl
                     << endl;
            }
        }
        else
        {
            string category = "";
            if (tech)
                category = "Technology";
            else if (business)
                category = "Business";
            else if (science)
                category = "Science";
            else if (sports)
                category = "Sports";
            else if (entertainment)
                category = "Entertainment";
            else if (politics)
                category = "Politics";
            else if (us)
                category = "US";
            else if (world)
                category = "World";

            vector<string> headlines = getCategoryNews(category, newsData);
            cout << "\n=== " << category << " News ===" << endl
                 << endl;
            for (string headline : headlines)
            {
                cout << headline << endl
                     << endl;
            }
        }
    }
    catch (const json::parse_error &e)
    {
        cerr << "Failed to parse JSON: " << e.what() << endl;
        return 1;
    }

    return 0;
}
