#include <boost/python.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <regex>
#include <algorithm>
#include <sstream>
#include <functional>

std::vector<std::string> split(const std::string str, const std::string regex_str)
{
    if(str.empty()) return std::vector<std::string>();
    std::regex regexz(regex_str);
    std::vector<std::string> list(std::sregex_token_iterator(str.begin(), str.end(), regexz, -1),
                                  std::sregex_token_iterator());
    return list;
}

template<typename Values = float>
class SparseVec
{
    // Attributs privés
    std::map<int, Values> dict;
public:
    //////////////////
    // Constructors //
    //////////////////
    
    // Void
    SparseVec(void) : dict() { }
    
    // Copy
    SparseVec(const SparseVec<Values> & sv) : dict(sv.dict) { }
        
    // From string-encoded map
    SparseVec(std::string str) {
        str.erase(remove(str.begin(), str.end(), ' '), str.end());
        str.erase(remove(str.begin(), str.end(), '{'), str.end());
        str.erase(remove(str.begin(), str.end(), '}'), str.end());
        auto dims = split(str,",");
        for(std::string token : dims) {
            auto tuple = split(token,":");
            int index = std::stoi(tuple[0]);
            Values val;
            std::istringstream ( tuple[1] ) >> val;
            dict[index] = val;
        }
    }
    
    // From python list
    SparseVec( boost::python::list v) { 
        for(int i = 0; i != boost::python::len(v); ++i)
            dict[i] = boost::python::extract<Values>(v[i]);
    }
    
    // From pyhon dict
    SparseVec( boost::python::dict d) { 
        boost::python::list keys = boost::python::list(d.keys());
        for (int i = 0; i < len(keys); ++i) {
            boost::python::extract<int> extractor(keys[i]);
            if (extractor.check()) {
                int key = extractor();
                dict[key] = boost::python::extract<Values>(d[key]);
            }
        }
    }
    
    
    //////////////////
    // Data access  //
    //////////////////

    // Set and get items (single value access for now)
    void set_item(int index, Values val) {dict[index] = val;}
    Values get_item(int index) { return dict[index]; }
    
    // Normalize representation
    std::map<int, Values> normalized(void) {
        std::map<int, Values> dict2;
        for( auto p : dict)
            if(p.second != 0) dict2[p.first] = p.second;
        return dict2;
    }
    
    // String representation
    std::string repr(void) {
        std::string str = "{";
        if(not dict.empty()) {
            std::ostringstream ostr;
            // remove null values
            dict = normalized();
            auto it = dict.begin();
            ostr << it->first << ":" << it->second;
            for(++it; it != dict.end(); ++it)
                ostr << "," << it->first << ":" << it->second;
            str += ostr.str();
        }
        str += "}";
        return str;
    }
    
    
    // Compute a known dimension lowerbound of the vector
    int get_dim(void) {
        int max = -1;
        for(auto p : dict) if(max<p.first) max = p.first;
        return max + 1;
    }

    // Dense c++ vector representation
    std::vector<Values> densify(void) {
        std::vector<Values> l;
        for(int i = 0; i < get_dim(); ++i)
            l.push_back(dict[i]);
        return l;
    }
    
    // Dense python list representation
    boost::python::list to_list(void) {
        boost::python::list l;
        for(int i = 0; i < get_dim(); ++i)
            l.append(dict[i]);
        return l;
    }
    
    
    // Dense python list representation
    boost::python::dict to_dict(void) {
        boost::python::dict d;
        for(auto p : dict)
            if(p.second != 0)
                d[p.first] = p.second;
        return d;
    }
    
    
    
    //////////////////
    // Arithmetic   //
    //////////////////
    
    
    // Arithmetic +=
    void iadd(SparseVec<Values> other) {
        for( auto p : other.dict )
            dict[p.first] += p.second;
        dict = normalized();
    }
    
    
    // Arithmetic +
    SparseVec<Values> add(SparseVec<Values> other) {
        SparseVec<Values> newvec(*this);
        newvec.iadd(other);
        return newvec;
    }

    // Arithmetic -=
    void isub(SparseVec<Values> other) {
        for( auto p : other.dict )
            dict[p.first] -= p.second;
        dict = normalized();
    }
    
    // Arithmetic -
    SparseVec<Values> sub(SparseVec<Values> other) {
        SparseVec<Values> newvec(*this);
        newvec.isub(other);
        return newvec;
    }

    // Arithmetic *=
    void imul(SparseVec<Values> other) {
        for( auto p : other.dict )
            dict[p.first] *= p.second;
        dict = normalized();
    }
    
    // Arithmetic *
    SparseVec<Values> mul(SparseVec<Values> other) {
        SparseVec<Values> newvec(*this);
        newvec.imul(other);
        return newvec;
    }
    
    
    
    //////////////////
    // Comparison   //
    //////////////////
    
    
    // Comparison generic
    template<typename Comp_fun>
    bool compare(SparseVec<Values> other, Comp_fun cmp) {
        bool ok = true;
        auto dict2 = other.normalized();
        auto it = dict.begin();
        while(ok and it != dict.end()) {
            ok = ok and cmp(it->second,dict2[it->first]);
            ++it;
        }
        it = dict2.begin();
        while(ok and it != dict2.end()) {
            ok = ok and cmp(dict[it->first],it->second);
            ++it;
        }
        return ok;
    }

    // Comparison ==
    bool eq(SparseVec<Values> other) {
        return compare(other, std::equal_to<Values>());
    }
    
    // Comparison !=
    bool neq(SparseVec<Values> other) {
        return not eq(other);
    }

    // Comparison <= (Pareto dominated)
    bool leq(SparseVec<Values> other) {
        return compare(other, std::less_equal<Values>() );
    }
    
    // Comparison >=
    bool geq(SparseVec<Values> other) {
        return compare(other, std::greater_equal<Values>() );        
    }
    
    // Comparison < (for non-null values only)
    bool lt(SparseVec<Values> other) {
        return compare(other, std::less<Values>() );
    }
    
    // Comparison > (for non-null values only)
    bool gt(SparseVec<Values> other) {
        return compare(other, std::greater<Values>() );        
    }
    
    

};
