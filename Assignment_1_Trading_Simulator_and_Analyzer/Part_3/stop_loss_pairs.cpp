#include <string>
#include <vector>
#include <cmath>

using namespace std;

string date_formatting_pairs_plus(string date)
{
    string s = "";
    s += date.substr(8, 2);
    s += "/";
    s += date.substr(5, 2);
    s += "/";
    s += date.substr(0, 4);
    return s;
}

double calculateMean_pairs_plus(const double arr[], int size)
{
    double sum = 0;
    for (int i = 0; i < size; ++i)
    {
        sum += arr[i];
    }
    return sum / size;
}

double calculateStandardDeviation_pairs_plus(const double arr[], int size, const double mean)
{
    double squaredDifferencesSum = 0;
    for (int i = 0; i < size; ++i)
    {
        double difference = arr[i] - mean;
        squaredDifferencesSum += difference * difference;
    }

    double meanSquaredDifferences = squaredDifferencesSum / size;
    return std::sqrt(meanSquaredDifferences);
}

double pairs_plus_strategy(const vector<vector<string>> &data1, const vector<vector<string>> &data2, vector<vector<string>> &CashFlow, vector<vector<string>> &order_stats1, vector<vector<string>> &order_stats2, int x, int n, double thresh, double stop_loss_thresh)
{

    order_stats1.push_back({"Date", "Order_dir", "Quantity", "Price"});
    order_stats2.push_back({"Date", "Order_dir", "Quantity", "Price"});
    CashFlow.push_back({"Date", "Cashflow"});
    int sign;

    int today_transaction;
    vector<pair<double, double>> store; // this stores the mean and std deviation of pevious days
                                        //  first is mean and second is standard deviation

    double spread_arr[n];
    for (int i = 0; i < n; i++)
    {
        spread_arr[i] = stod(data1[i][1]) - stod(data2[i][1]);
    }

    int curr_pos_at_start;
    int curr_pos = 0;
    double cumulative_cashflow = 0.0;
    double rolling_mean, rolling_std_dev, z_score, spread_today;

    int data_length = data1.size() - 1;
    for (int i = n; i < data_length; i++)
    {
        curr_pos_at_start = curr_pos;
        spread_today = stod(data1[i][1]) - stod(data2[i][1]);
        spread_arr[i % n] = spread_today;
        rolling_mean = calculateMean_pairs_plus(spread_arr, n);
        rolling_std_dev = calculateStandardDeviation_pairs_plus(spread_arr, n, rolling_mean);
        z_score = (spread_today - rolling_mean) / rolling_std_dev;
        string date = date_formatting_pairs_plus(data1[i][0]);
        vector<string> CashFlow_row;

        if (z_score < -thresh)
        {
            if (curr_pos < x)
            {
                curr_pos++;
                if (curr_pos < 0)
                {
                    // need to remove the value from store
                    store.erase(store.begin());
                }
                else
                {
                    // need to push_back the values to store array;
                    store.push_back(make_pair(rolling_mean, rolling_std_dev));
                }
            }
        }
        else if (z_score > thresh)
        {
            if (curr_pos > -x)
            {
                curr_pos--;
                if (curr_pos > 0)
                {
                    // need to remove the value from store
                    store.erase(store.begin());
                }
                else
                {
                    // need to push_back the values to store array;
                    store.push_back(make_pair(rolling_mean, rolling_std_dev));
                }
            }
        }

        // these lower 3 conditions are important , we are calculating the sign of curr_pos after sell/buy transaction
        // I will use these to calculate curr_position at the end of the day
        if (curr_pos == 0)
        {
            sign = 0;
        }
        else if (curr_pos > 0)
        {
            sign = 1;
        }
        else
        {
            sign = -1;
        }

        double z_score_store;

        // removing the previous positions by comapring their new z_score with stop_loss_threshold
        for (int i = store.size() - 1; i >= 0; i--)
        {
            z_score_store = (spread_today - store[i].first) / store[i].second;
            if (abs(z_score_store) > stop_loss_thresh)
            {
                store.erase(store.begin() + i);
            }
        }

        curr_pos = sign * store.size();
        int change = curr_pos - curr_pos_at_start;      // change in position
        cumulative_cashflow -= (change * spread_today); // updating cashflow using today's transaction

        if (change > 0)
        {
            vector<string> order_stats_row1;
            vector<string> order_stats_row2;

            order_stats_row1.push_back(date);
            order_stats_row1.push_back("BUY");
            order_stats_row1.push_back(to_string(change));
            order_stats_row1.push_back(data1[i][1]);

            order_stats_row2.push_back(date);
            order_stats_row2.push_back("SELL");
            order_stats_row2.push_back(to_string(change));
            order_stats_row2.push_back(data2[i][1]);

            order_stats1.push_back(order_stats_row1);
            order_stats2.push_back(order_stats_row2);
        }
        else if (change < 0)
        {
            vector<string> order_stats_row1;
            vector<string> order_stats_row2;

            order_stats_row1.push_back(date);
            order_stats_row1.push_back("SELL");
            order_stats_row1.push_back("1");
            order_stats_row1.push_back(data1[i][1]);

            order_stats_row2.push_back(date);
            order_stats_row2.push_back("BUY");
            order_stats_row2.push_back("1");
            order_stats_row2.push_back(data2[i][1]);

            order_stats1.push_back(order_stats_row1);
            order_stats2.push_back(order_stats_row2);
        }

        CashFlow_row.push_back(date);
        CashFlow_row.push_back(to_string(cumulative_cashflow));
        CashFlow.push_back(CashFlow_row);
    }

    cumulative_cashflow += curr_pos * spread_today;
    return cumulative_cashflow;
}