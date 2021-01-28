CXX=@g++
CXXFLAGS=-g -Wall -std=c++11 -D_DEBUG

EXEC=src
SRCS=$(wildcard *.cpp)
OBJDIR=.build
OBJS=$(patsubst %.cpp,$(OBJDIR)/%.o,$(SRCS))

$(EXEC): $(OBJS)
	@$(CXX) $(OBJS) -o $(OBJDIR)/$(EXEC)

$(OBJDIR)/%.o: %.cpp
	@mkdir -p $(OBJDIR)
	@$(CXX) -c $(CXXFLAGS) $< -o $@

test: $(EXEC)
	@./$(OBJDIR)/src < sample.txt

debug: $(EXEC)
	@lldb -f ./$(OBJDIR)/src -o "break set -E C++" -o "proc launch -i sample.txt"

clean:
	@rm -rf $(OBJDIR) 
